"""Run one Group 3 condition, or one short smoke run, with HF Trainer."""

import argparse
import csv
import hashlib
import importlib.metadata as metadata
import json
import re
import tempfile
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score
from torch.utils.data import Dataset
from transformers import (
    AutoModelForSequenceClassification, AutoTokenizer, BitsAndBytesConfig,
    DataCollatorWithPadding, Trainer, TrainingArguments, set_seed,
)
from peft import IA3Config, LoraConfig, get_peft_model, prepare_model_for_kbit_training

from track3_preflight import audit_data

HERE = Path(__file__).resolve().parent
LABELS = ["Positive", "Negative", "Objective"]
BUNDLE_FILES = ("train_group3.py", "collect_results.py", "track3_preflight.py",
                "track3_preflight.json", "group3_run_plan.json", "colab_requirements.txt")
REVISIONS = {
    "xlm-roberta-base": ("FacebookAI/xlm-roberta-base", "e73636d4f797dec63c3081bb6ed5c7b0bb3f2089"),
    "google/muril-base-cased": ("google/muril-base-cased", "afd9f36c7923d54e97903922ff1b260d091d202f"),
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path, data):
    path = Path(path)
    staged = path.with_suffix(".tmp")
    staged.write_text(json.dumps(data, indent=2, allow_nan=False), encoding="utf-8")
    staged.replace(path)


def job_id(row):
    model = "xlmr" if row["model"] == "xlm-roberta-base" else "muril"
    return f"{model}_{row['experiment']}_{row['method']}_{row['seed']}_{round(100*row['fraction']):03d}"


def bundle_hash():
    files = {name: (HERE / name).read_text(encoding="utf-8-sig") for name in BUNDLE_FILES}
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def target_names(model, exp):
    names = [name for name, _ in model.named_modules()]
    projections = ("key", "value") if exp.startswith("07") else ("query", "value")
    targets = [name for name in names if name.endswith(tuple(".attention.self." + p for p in projections))]
    ffn = [name for name in names if re.search(r"\.encoder\.layer\.\d+\.output\.dense$", name)]
    layers = model.config.num_hidden_layers
    if len(targets) != 2 * layers or len(ffn) != layers:
        raise ValueError("Unexpected attention or FFN module count. Inspect model.named_modules().")
    return targets + (ffn if exp in ("04", "07b") else []), ffn if exp == "07b" else []


def make_model(model_id, revision, exp):
    kwargs = dict(revision=revision, num_labels=len(LABELS),
                  id2label=dict(enumerate(LABELS)), label2id={v: k for k, v in enumerate(LABELS)})
    quantized = exp in ("05", "06")
    if quantized:
        kwargs.update(
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.float16, llm_int8_skip_modules=["classifier"],
            ),
            device_map={"": 0},
        )
    model = AutoModelForSequenceClassification.from_pretrained(model_id, **kwargs)
    if exp == "01":
        return model, []
    targets, ffn = target_names(model, exp)
    if quantized:
        model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=False)
    common = dict(task_type="SEQ_CLS", target_modules=targets, modules_to_save=["classifier"])
    if exp.startswith("07"):
        config = IA3Config(**common, feedforward_modules=ffn)
    else:
        config = LoraConfig(**common, r=8 if exp == "02" else 16,
                            lora_alpha=16, lora_dropout=0.0, bias="none")
    model = get_peft_model(model, config)
    names = [name for name, p in model.named_parameters() if p.requires_grad]
    prefix = "ia3_" if exp.startswith("07") else "lora_"
    if (not any(prefix in n for n in names) or not any("classifier" in n for n in names)
            or any(prefix not in n and "classifier" not in n for n in names)):
        raise ValueError("Expected trainable adapters and classification head only.")
    if any(p.requires_grad for p in model.parameters() if type(p).__name__ == "Params4bit"):
        raise ValueError("A packed quantized base weight is trainable.")
    return model, targets


class TextRows(Dataset):
    def __init__(self, ids, rows, tokenizer, max_length):
        self.tokenized = tokenizer([rows[i][0] for i in ids], truncation=True, max_length=max_length)
        self.labels = [LABELS.index(rows[i][1]) for i in ids]

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, i):
        return {**{k: v[i] for k, v in self.tokenized.items()}, "labels": self.labels[i]}


def score(predictions, labels):
    return {"macro_f1": float(f1_score(labels, predictions, average="macro",
                                       labels=range(len(LABELS)), zero_division=0)),
            "accuracy": float(accuracy_score(labels, predictions))}


def trainer_metrics(output):
    return score(np.argmax(output.predictions, axis=1), output.label_ids)


def export_predictions(trainer, data, ids, destination):
    trainer.compute_metrics = None
    output = trainer.predict(data)
    prediction = output.predictions.argmax(1).tolist()
    labels = output.label_ids.tolist()
    with destination.open("w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["source_row_id", "label", "prediction"])
        writer.writerows(zip(ids, labels, prediction))
    return score(prediction, labels) if destination.name == "validation_predictions.csv" else None


@torch.no_grad()
def smoke_reload(trainer, dataset, folder):
    """Round-trip the actual trainable tensors and verify the same logits."""
    model = trainer.model
    model.eval()
    device = next(model.parameters()).device
    batch = {key: value.to(device) for key, value in trainer.data_collator([dataset[0], dataset[1]]).items()}
    assert all(0 <= x < len(LABELS) for x in batch["labels"].tolist())
    before = model(**batch).logits
    assert before.shape == (2, len(LABELS)) and bool(torch.isfinite(before).all())
    params = {n: p for n, p in model.named_parameters() if p.requires_grad}
    path = Path(folder) / "smoke_weights.pt"
    torch.save({n: p.detach().cpu() for n, p in params.items()}, path)
    next(iter(params.values())).zero_()
    weights = torch.load(path, map_location="cpu", weights_only=True)
    for name, values in weights.items():
        params[name].copy_(values)
    after = model(**batch).logits
    torch.testing.assert_close(after, before, atol=1e-5, rtol=1e-5)
    return {"logits_shape": list(after.shape), "saved_reloaded_trainable_tensors": len(weights)}


def run(row, root, exp, microbatch, smoke):
    if not torch.cuda.is_available() or "T4" not in torch.cuda.get_device_name(0):
        raise RuntimeError("Use a Colab T4 GPU runtime.")
    torch.set_num_threads(2)
    set_seed(row["seed"])
    plan = read_json(HERE / "group3_run_plan.json")
    audit = read_json(HERE / "track3_preflight.json")
    actual, all_rows = audit_data(include_all=True)
    for key in ("sha256", "splits", "reduced_train_subsets"):
        if json.loads(json.dumps(actual[key])) != audit[key]:
            raise ValueError(f"Recomputed {key} differs; verify the pinned data and scikit-learn.")
    rows = {i: (text, label) for i, text, label in all_rows}
    sizes = audit["splits"]
    train_ids = sizes["train"]["source_row_ids"]
    if row["fraction"] != 1:
        pct = f"{round(100 * row['fraction'])}%"
        train_ids = audit["reduced_train_subsets"][str(row["seed"])][pct]["source_row_ids"]
    model_id, revision = REVISIONS[row["model"]]
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    max_length = plan["max_length"]
    train = TextRows(train_ids, rows, tokenizer, max_length)
    val = TextRows(sizes["validation"]["source_row_ids"], rows, tokenizer, max_length)
    model, targets = make_model(model_id, revision, exp)
    trainables = {n: p.numel() for n, p in model.named_parameters() if p.requires_grad}
    count = sum(trainables.values())
    optimizer = "adamw_torch"
    if exp in ("05", "06"):
        from bitsandbytes.optim import AdamW
        optimizer = "bnb_adamw_32bit_paged" if exp == "05" else "bnb_adamw_32bit_unpaged"
        opt_cls = (AdamW, {"optim_bits": 32, "is_paged": exp == "05"})
    else:
        opt_cls = None
    destination = root / ("smoke" if smoke else "runs") / job_id(row)
    destination.mkdir(parents=True, exist_ok=True)
    config = dict(row, effective_experiment=exp, trainer_optimizer=optimizer,
                  model_revision=revision, max_length=max_length, train_n=len(train),
                  microbatch=microbatch, grad_accumulation=16 // microbatch, seed=row["seed"],
                  evaluation_policy="final_epoch_in_memory", padding="dynamic", fp16=True,
                  scheduler="linear", warmup_steps=0, weight_decay=0.0, max_grad_norm=1.0,
                  quantization="nf4_double_quant_fp16" if exp in ("05", "06") else "none",
                  adapter_rank=(8 if exp == "02" else 16) if exp in ("02","03","04","05","06") else None,
                  adapter_alpha=16 if exp in ("02","03","04","05","06") else None,
                  unpadded_tokens_per_epoch=sum(len(x) for x in train.tokenized["input_ids"]),
                  dataset_sha256=audit["sha256"],
                  source_bundle_sha256=bundle_hash(), adapter_targets=targets,
                  train_subset_sha256=hashlib.sha256(json.dumps(sorted(train_ids)).encode()).hexdigest(),
                  gpu=torch.cuda.get_device_name(0), cuda=torch.version.cuda,
                  versions={p: metadata.version(p) for p in (
                      "torch", "transformers", "peft", "accelerate", "bitsandbytes", "scikit-learn")})
    write_json(destination / "config.json", config)
    write_json(destination / "parameter_audit.json", {"targets": targets, "trainable": trainables})
    with tempfile.TemporaryDirectory() as scratch:
        # Final epoch only; no early stopping or test-set model selection.
        args = TrainingArguments(
            output_dir=scratch, num_train_epochs=3, max_steps=1 if smoke else -1,
            per_device_train_batch_size=microbatch, per_device_eval_batch_size=16,
            gradient_accumulation_steps=16 // microbatch,
            learning_rate=row["lr"], fp16=True, bf16=False, report_to=[],
            save_strategy="no", eval_strategy="no", logging_steps=10, logging_first_step=True,
            logging_nan_inf_filter=False, include_num_input_tokens_seen=True,
            seed=row["seed"], data_seed=row["seed"], disable_tqdm=True,
        )
        trainer = Trainer(model=model, args=args, train_dataset=train, eval_dataset=val,
                          processing_class=tokenizer, data_collator=DataCollatorWithPadding(tokenizer),
                          compute_metrics=trainer_metrics, optimizer_cls_and_kwargs=opt_cls)
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
        initial_bytes = torch.cuda.memory_allocated()
        start = time.perf_counter()
        trained = trainer.train()
        torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        peak = torch.cuda.max_memory_allocated()
        if (not np.isfinite(trained.training_loss) or trained.training_loss <= 0
                or any(not bool(torch.isfinite(p).all()) for p in model.parameters() if p.requires_grad)):
            raise ValueError("Invalid training loss; inspect gradients and precision.")
        if not smoke:
            val_ids = sizes["validation"]["source_row_ids"]
            validation = export_predictions(trainer, val, val_ids, destination / "validation_predictions.csv")
            test_ids = sizes["test"]["source_row_ids"]
            test = TextRows(test_ids, rows, tokenizer, max_length)
            # No held-out metrics computed here. The selector reads only validation evidence.
            export_predictions(trainer, test, test_ids, destination / "heldout_predictions.csv")
            reload_check = None
        else:
            validation = {}
            reload_check = smoke_reload(trainer, val, scratch)
        write_json(destination / "trainer_log.json", trainer.state.log_history)
    result = dict(config, status="smoke_pass" if smoke else "complete", trainable_params=count,
                  train_seconds=elapsed, initial_allocated_bytes=initial_bytes, peak_bytes=peak,
                  global_steps=trained.global_step, epoch_reached=trainer.state.epoch,
                  padded_input_tokens_seen=trainer.state.num_input_tokens_seen,
                  training_loss=trained.training_loss, reload_check=reload_check,
                  val_macro_f1=validation.get("macro_f1"), val_accuracy=validation.get("accuracy"))
    write_json(destination / "result.json", result)
    print(job_id(row), result["status"], "seconds", round(elapsed, 1), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_id")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--microbatch", type=int, choices=(1, 2, 4, 8, 16), default=8)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    jobs = {job_id(j): j for j in read_json(HERE / "group3_run_plan.json")["jobs"]}
    row = jobs[args.job_id]
    exp = row["experiment"]
    if exp == "08":
        choices = read_json(args.output / "validation_selection.json")["choices"]
        exp = choices[row["model"]][row["method"]]
    folder = args.output / ("smoke" if args.smoke else "runs") / args.job_id
    if (folder / "result.json").exists():
        saved = read_json(folder / "result.json")
        if (saved.get("source_bundle_sha256") != bundle_hash()
                or saved.get("microbatch") != args.microbatch
                or saved.get("effective_experiment") != exp):
            raise ValueError("Saved job differs from this bundle or config. Use a new evidence directory.")
        print("Completed evidence preserved:", args.job_id)
        return
    try:
        run(row, args.output, exp, args.microbatch, args.smoke)
    except Exception as error:
        folder.mkdir(parents=True, exist_ok=True)
        previous = list(folder.glob("failure_*.json"))
        write_json(folder / f"failure_{len(previous)+1:03d}.json",
                   {"job": row, "effective_experiment": exp, "microbatch": args.microbatch,
                    "error_type": type(error).__name__, "message": str(error), "status": "failed"})
        raise


if __name__ == "__main__":
    main()
