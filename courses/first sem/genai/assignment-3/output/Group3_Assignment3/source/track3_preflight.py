"""Audit the original Track 3 data and optionally measure both tokenizers.

No model weights are loaded and no model training is done.
"""

import argparse
import csv
import hashlib
import io
import json
import math
import re
from collections import Counter, defaultdict
from urllib.request import urlopen

from sklearn import __version__ as sklearn_version
from sklearn.model_selection import train_test_split

REVISION = "8718cf9d03f16c90006f4e61fb5009164f5cf25f"
SOURCE = ("https://raw.githubusercontent.com/MuhammadYaseenKhan/"
          f"Urdu-Sentiment-Corpus/{REVISION}/urdu-sentiment-corpus-v1.tsv")
SHA256 = "c76a97fbb8557a1ff7db7e858138c0002a905d6d45d611773fb1b0ee5737136a"
LABELS = {"P": "Positive", "N": "Negative", "O": "Objective"}
MODELS = ("FacebookAI/xlm-roberta-base", "google/muril-base-cased")


def clean(text):
    text = re.sub(r"https?://\S+|www\.\S+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"(?<!\w)@\w+", " ", text)
    text = text.translate(str.maketrans({"ي": "ی", "ك": "ک"}))
    return " ".join(text.split())


def audit_data(include_all=False):
    with urlopen(SOURCE, timeout=30) as response:
        raw = response.read()
    if hashlib.sha256(raw).hexdigest() != SHA256:
        raise ValueError("Dataset file differs from the verified author release.")
    reader = csv.reader(io.StringIO(raw.decode("utf-8-sig")), delimiter="\t", quoting=csv.QUOTE_NONE)
    if next(reader) != ["Tweet", "Class"]:
        raise ValueError("Unexpected TSV schema.")
    groups = defaultdict(list)
    stats = Counter()
    for row_id, row in enumerate(reader, start=2):
        stats["source_rows"] += 1
        if len(row) != 2 or row[1].strip() not in LABELS:
            stats["malformed_or_invalid_label"] += 1
            continue
        text = clean(row[0])
        if not text:
            stats["empty_after_cleaning"] += 1
            continue
        groups[text].append((row_id, LABELS[row[1].strip()]))
    rows = []
    for text, entries in groups.items():
        if len({label for _, label in entries}) > 1:
            stats["rows_with_conflicting_labels"] += len(entries)
            continue
        stats["duplicate_rows_removed"] += len(entries) - 1
        row_id, label = entries[0]
        rows.append((row_id, text, label))
    rows.sort()
    train, remainder = train_test_split(rows, test_size=0.30, random_state=3,
                                        stratify=[row[2] for row in rows])
    validation, test = train_test_split(remainder, test_size=0.5, random_state=3,
                                        stratify=[row[2] for row in remainder])
    splits = {"train": train, "validation": validation, "test": test}
    assert sum(map(len, splits.values())) == len({r[1] for v in splits.values() for r in v})
    assert all(set(r[2] for r in v) == set(LABELS.values()) for v in splits.values())
    assert sum(stats.values()) - stats["source_rows"] + len(rows) == stats["source_rows"]
    report = {"status": "preflight_only", "group_working_assumption": 3, "track": 3,
              "split_seed": 3, "run_seeds": [3, 103], "source": SOURCE, "sha256": SHA256,
              "sklearn_version": sklearn_version,
              "cleaning_counts": dict(stats), "clean_rows": len(rows),
              "splits": {key: {"count": len(value), "labels": dict(Counter(r[2] for r in value)),
                               "source_row_ids": [r[0] for r in value]}
                         for key, value in splits.items()},
              "reduced_train_subsets": {seed: reduced_subsets(train, seed) for seed in (3, 103)}}
    return report, rows if include_all else train


def reduced_subsets(train, seed):
    half, _ = train_test_split(train, train_size=len(train) // 2, random_state=seed,
                                stratify=[row[2] for row in train])
    quarter, _ = train_test_split(half, train_size=len(train) // 4, random_state=seed,
                                   stratify=[row[2] for row in half])
    return {label: {"count": len(rows), "labels": dict(Counter(row[2] for row in rows)),
                    "source_row_ids": sorted(row[0] for row in rows)}
            for label, rows in (("25%", quarter), ("50%", half))}


def audit_tokenizers(train):
    from transformers import AutoConfig, AutoTokenizer, __version__ as transformers_version
    from tokenizers import __version__ as tokenizers_version
    from huggingface_hub import HfApi

    texts = [row[1] for row in train]
    words = sum(len(text.split()) for text in texts)
    output, lengths_by_model, limits = {}, {}, []
    for model in MODELS:
        revision = HfApi().model_info(model).sha
        tokenizer = AutoTokenizer.from_pretrained(model, revision=revision, use_fast=True)
        config = AutoConfig.from_pretrained(model, revision=revision)
        limits.append(min(tokenizer.model_max_length, config.max_position_embeddings,
                          512))  # Both released encoders support up to 512 tokens.
        ids = tokenizer(texts, add_special_tokens=False, truncation=False)["input_ids"]
        lengths = [len(seq) + tokenizer.num_special_tokens_to_add(pair=False) for seq in ids]
        tokens = sum(map(len, ids))
        unknown = sum(seq.count(tokenizer.unk_token_id) for seq in ids)
        lengths_by_model[model] = lengths
        output[model] = {
            "revision": revision, "train_words": words, "subword_tokens": tokens,
            "unknown_tokens": unknown, "fertility": tokens / words,
            "unknown_rate": unknown / tokens,
            "p95_nearest_rank": sorted(lengths)[math.ceil(0.95 * len(lengths)) - 1],
        }
    max_length = min(max(row["p95_nearest_rank"] for row in output.values()), min(limits))
    for model, values in output.items():
        above = sum(length > max_length for length in lengths_by_model[model])
        values["texts_truncated"] = above
        values["truncation_rate"] = above / len(texts)
    return {"max_length": max_length, "analysis_split": "train", "models": output,
            "transformers_version": transformers_version, "tokenizers_version": tokenizers_version}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizers", action="store_true", help="fetch tokenizer files only")
    args = parser.parse_args()
    report, train_rows = audit_data()
    if args.tokenizers:
        report["tokenizers"] = audit_tokenizers(train_rows)
    print(json.dumps(report, indent=2))
