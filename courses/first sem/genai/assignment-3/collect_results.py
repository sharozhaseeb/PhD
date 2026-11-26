"""Select on validation; then verify and aggregate completed held-out runs."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import mean, stdev

from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support

HERE = Path(__file__).resolve().parent
LABELS = ["Positive", "Negative", "Objective"]


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def job_id(job):
    model = "xlmr" if job["model"] == "xlm-roberta-base" else "muril"
    return f"{model}_{job['experiment']}_{job['method']}_{job['seed']}_{round(100*job['fraction']):03d}"


def completed(root, job):
    folder = root / "runs" / job_id(job)
    row = load(folder / "result.json")
    if row["status"] != "complete" or any(row[k] != value for k, value in job.items()):
        raise ValueError(f"Result provenance mismatch: {folder}")
    if row["microbatch"] * row["grad_accumulation"] != 16:
        raise ValueError(f"Wrong effective batch: {folder}")
    if ("T4" not in row["gpu"] or not math.isclose(row["epoch_reached"], 3)
            or row["global_steps"] != 3 * math.ceil(row["train_n"] / 16)
            or row["padded_input_tokens_seen"] < 3 * row["unpadded_tokens_per_epoch"]
            or not all(math.isfinite(row[k]) and row[k] > 0 for k in (
                "train_seconds", "peak_bytes", "training_loss", "trainable_params"))):
        raise ValueError(f"Incomplete or invalid T4 run: {folder}")
    config = load(folder / "config.json")
    if config != {k: row[k] for k in config}:
        raise ValueError(f"Saved run/config differ: {folder}")
    params = load(folder / "parameter_audit.json")
    if params["targets"] != row["adapter_targets"] or sum(params["trainable"].values()) != row["trainable_params"]:
        raise ValueError(f"Parameter audit differs: {folder}")
    exp = row["effective_experiment"]
    if exp != "01":
        expected = 36 if exp in ("04", "07b") else 24
        if len(params["targets"]) != expected or not any("classifier" in n for n in params["trainable"]):
            raise ValueError(f"Unexpected adaptation targets or frozen head: {folder}")
    return row, folder


def read_predictions(path, expected_ids, truth=None):
    with path.open(newline="") as fp:
        prediction_rows = list(csv.DictReader(fp))
    ids = [int(p["source_row_id"]) for p in prediction_rows]
    labels = [int(p["label"]) for p in prediction_rows]
    predicted = [int(p["prediction"]) for p in prediction_rows]
    if ids != expected_ids or not set(labels + predicted) <= {0, 1, 2}:
        raise ValueError(f"Unexpected IDs or class values in {path}")
    if truth is not None and labels != [truth[i] for i in ids]:
        raise ValueError(f"Gold labels differ from the original file in {path}")
    return labels, predicted


def select(root, plan):
    groups = {}
    audit = load(HERE / "track3_preflight.json")
    val_ids = audit["splits"]["validation"]["source_row_ids"]
    for job in plan["jobs"]:
        if job["fraction"] != 1:
            continue
        row, folder = completed(root, job)
        labels, predicted = read_predictions(folder / "validation_predictions.csv", val_ids)
        checked = f1_score(labels, predicted, labels=[0, 1, 2], average="macro", zero_division=0)
        if not math.isclose(checked, row["val_macro_f1"], abs_tol=1e-10):
            raise ValueError(f"Validation metric differs from raw predictions: {folder}")
        key = (row["model"], row["method"], row["experiment"])
        groups.setdefault(key, {})[row["seed"]] = row["val_macro_f1"]
    choices, values = {}, {}
    for (model, method, exp), scores in sorted(groups.items()):
        assert set(scores) == set(plan["seeds"])
        metric = mean(scores.values())
        if metric > values.get((model, method), -1):
            values[(model, method)] = metric
            choices.setdefault(model, {})[method] = exp
    record = {"choices": choices, "rule": "highest mean validation macro-F1; ties use first experiment",
              "validation_scores": [{"model": k[0], "method": k[1], "experiment": k[2],
                                     "by_seed": v} for k, v in sorted(groups.items())]}
    path = root / "validation_selection.json"
    stable_record = json.loads(json.dumps(record))
    if path.exists():
        if load(path) != stable_record:
            raise ValueError("Existing frozen validation selection differs.")
    else:
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return stable_record


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def aggregate(root, plan):
    from track3_preflight import audit_data

    selection = select(root, plan)
    audit = load(HERE / "track3_preflight.json")
    actual, raw = audit_data(include_all=True)
    if actual["sha256"] != audit["sha256"]:
        raise ValueError("Data source hash differs.")
    truth = {i: LABELS.index(label) for i, _, label in raw}
    expected_ids = audit["splits"]["test"]["source_row_ids"]
    val_ids = audit["splits"]["validation"]["source_row_ids"]
    rows, buckets, per_class = [], {}, []
    comparable = ("macro_f1", "accuracy", "train_seconds", "peak_mib", "trainable_params")
    for job in plan["jobs"]:
        row, folder = completed(root, job)
        expected_exp = job["experiment"]
        if expected_exp == "08":
            expected_exp = selection["choices"][job["model"]][job["method"]]
        if row["effective_experiment"] != expected_exp or row["max_length"] != plan["max_length"]:
            raise ValueError(f"Unexpected configuration at {folder}")
        ids = (audit["splits"]["train"]["source_row_ids"] if row["fraction"] == 1 else
               audit["reduced_train_subsets"][str(row["seed"])][f"{round(100*row['fraction'])}%"]["source_row_ids"])
        subset = hashlib.sha256(json.dumps(sorted(ids)).encode()).hexdigest()
        if len(ids) != row["train_n"] or subset != row["train_subset_sha256"]:
            raise ValueError(f"Unexpected training subset at {folder}")
        read_predictions(folder / "validation_predictions.csv", val_ids, truth)
        labels, predicted = read_predictions(folder / "heldout_predictions.csv", expected_ids, truth)
        p, r, f, s = precision_recall_fscore_support(labels, predicted, labels=[0, 1, 2], zero_division=0)
        for i, name in enumerate(LABELS):
            per_class.append({"job": job_id(job), "label": name, "precision": p[i], "recall": r[i],
                              "f1": f[i], "support": s[i]})
        config = {**row, "versions": json.dumps(row["versions"], sort_keys=True),
                  "adapter_targets": json.dumps(row["adapter_targets"]),
                  "attempt_failures": len(list(folder.glob("failure_*.json"))),
                  "group": plan["group"], "track": plan["track"],
                  "macro_f1": f1_score(labels, predicted, labels=[0, 1, 2], average="macro", zero_division=0),
                  "accuracy": accuracy_score(labels, predicted), "test_n": len(labels),
                  "peak_mib": row["peak_bytes"] / 1024**2}
        rows.append(config)
        key = (row["model"], row["method"], row["experiment"], row["fraction"])
        buckets.setdefault(key, []).append(config)
    summaries = []
    for field in ("source_bundle_sha256", "microbatch", "versions", "gpu", "evaluation_policy"):
        if len({row[field] for row in rows}) != 1:
            raise ValueError(f"Full roster must use a common {field}.")
    for (model, method, exp, fraction), group in sorted(buckets.items()):
        if sorted(row["seed"] for row in group) != sorted(plan["seeds"]):
            raise ValueError("Both seeds are required.")
        metrics = {}
        for name in comparable:
            values = [row[name] for row in group]
            metrics[name + "_mean"] = mean(values)
            metrics[name + "_sd"] = stdev(values)
        summaries.append(dict(model=model, method=method, experiment=exp,
                              effective_experiment=group[0]["effective_experiment"], fraction=fraction, **metrics))
    write_csv(root / "results.csv", rows)
    write_csv(root / "summary.csv", summaries)
    write_csv(root / "per_class.csv", per_class)
    print(f"Verified {len(rows)} completed runs and wrote {len(summaries)} paired summaries.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--select-only", action="store_true")
    args = parser.parse_args()
    plan = load(HERE / "group3_run_plan.json")
    if args.select_only:
        print(json.dumps(select(args.output, plan)["choices"], indent=2))
    else:
        aggregate(args.output, plan)
