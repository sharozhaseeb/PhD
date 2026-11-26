"""Print the planned Assignment 3 job matrix as JSON; never runs training."""

import argparse
import json
from pathlib import Path

DATASETS = {
    1: ("roman_urdu", ("sentiment",)),
    2: ("roman_urdu_hate_speech", ("Coarse_Grained", "Fine_Grained")),
    3: ("urdu_sentiment_corpus", ("sentiment",)),
    4: ("urdu_fake_news", ("fake_news",)),
}
MODELS = ("xlm-roberta-base", "google/muril-base-cased")
CONFIGS = (
    ("01", "full_ft", "baseline"),
    ("02", "lora", "rank8_qv"),
    ("03", "lora", "rank16_qv"),
    ("04", "lora", "rank16_qv_ffn"),
    ("05", "qlora", "nf4_double_quant_rank16_paged"),
    ("06", "qlora", "nf4_double_quant_rank16_nonpaged"),
    ("07a", "ia3", "kv"),
    ("07b", "ia3", "kv_ffn"),
)


def make_plan(group):
    if group < 1:
        raise ValueError("Use the assigned positive group number.")
    track = (group - 1) % 4 + 1
    seeds = [group, group + 100]
    dataset, tasks = DATASETS[track]
    fractions = (0.10, 0.30) if track in (1, 2) else (0.25, 0.50)
    rows = []
    for task in tasks:
        for model in MODELS:
            for seed in seeds:
                shared = {"task": task, "model": model, "seed": seed, "epochs": 3,
                          "effective_batch_size": 16}
                for experiment, method, setting in CONFIGS:
                    lr = 2e-5 if method == "full_ft" else 2e-4
                    rows.append(dict(shared, experiment=experiment, method=method,
                                     setting=setting, fraction=1.0, lr=lr))
                for method in ("full_ft", "lora", "qlora", "ia3"):
                    for fraction in fractions:
                        lr = 2e-5 if method == "full_ft" else 2e-4
                        rows.append(dict(shared, experiment="08", method=method, fraction=fraction,
                                         setting="pending_validation_selection", lr=lr))
    return {"group": group, "track": track, "seeds": seeds,
            "dataset": "community-datasets/" + dataset, "tasks": list(tasks),
            "max_length": None, "status": "planning_only", "jobs": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", type=int, help="assigned group number")
    parser.add_argument("--preflight", type=Path, help="optional audit with measured max_length")
    args = parser.parse_args()
    try:
        plan = make_plan(args.group)
        if args.preflight:
            report = json.loads(args.preflight.read_text(encoding="utf-8-sig"))
            if report["group_working_assumption"] != args.group or report["track"] != plan["track"]:
                raise ValueError("The audit must match the group and track.")
            plan["max_length"] = report["tokenizers"]["max_length"]
            plan["data_audit"] = args.preflight.name
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(plan, indent=2))
