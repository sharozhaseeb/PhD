"""Generate the five required plots after validating all real experiment rows."""

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from collect_results import HERE, aggregate, load, select

MODELS = {"xlm-roberta-base": "XLM-R", "google/muril-base-cased": "MuRIL"}
METHODS = {"full_ft": "Full FT", "lora": "LoRA", "qlora": "QLoRA", "ia3": "IA3"}
COLORS = dict(zip(METHODS, ("#235789", "#168272", "#b25923", "#7657a5")))


def plot_results(root):
    plan = load(HERE / "group3_run_plan.json")
    audit = load(HERE / "track3_preflight.json")
    aggregate(root, plan)
    choices = select(root, plan)["choices"]
    with (root / "summary.csv").open(newline="") as fp:
        rows = list(csv.DictReader(fp))
    full = [r for r in rows if r["experiment"] != "08"]
    lookup = {(r["model"], r["experiment"]): r for r in full}
    folder = root / "figures"
    folder.mkdir(exist_ok=True)

    def save(fig, name):
        fig.tight_layout()
        fig.savefig(folder / name, dpi=190)
        plt.close(fig)

    def f1(row):
        return float(row["macro_f1_mean"])

    def error(row):
        return float(row["macro_f1_sd"])

    def costs(fig_name, metric, xlabel):
        fig, ax = plt.subplots(figsize=(7.6, 4.5))
        points = []
        shapes = {"xlm-roberta-base": "o", "google/muril-base-cased": "s"}
        for r in rows:
            x, y = float(r[metric + "_mean"]), f1(r)
            points.append((x, y))
            is_full = r["experiment"] != "08"
            ax.errorbar(x, y, xerr=float(r[metric + "_sd"]), yerr=error(r),
                        color=COLORS[r["method"]], marker=shapes[r["model"]], linestyle="",
                        alpha=1 if is_full else 0.32)
            if is_full and r["model"] == "xlm-roberta-base" and r["experiment"] in ("01", "04", "05"):
                ax.annotate(MODELS[r["model"]][0] + r["experiment"], (x, y),
                            xytext=(-7, 6), textcoords="offset points", ha="right", fontsize=8)
        frontier = sorted(set((x, y) for x, y in points if not any(
            a <= x and b >= y and (a < x or b > y) for a, b in points)))
        frontier_line, = ax.plot(*zip(*frontier), linestyle="--", color="#222222", label="Nondominated means")
        ax.set(xlabel=xlabel, ylabel="Test macro-F1", title="All configurations (mean ± sample SD)")
        methods = [Line2D([], [], color=COLORS[method], marker="o", linestyle="", label=label)
                   for method, label in METHODS.items()]
        ax.legend(handles=[*methods, frontier_line], loc="upper center", bbox_to_anchor=(0.5, -0.18),
                  ncol=5, fontsize=8, frameon=False)
        save(fig, fig_name)

    fig, ax = plt.subplots(figsize=(6, 3.2))
    for model, label in MODELS.items():
        pair = [lookup[(model, exp)] for exp in ("02", "03")]
        ax.errorbar([8, 16], [f1(r) for r in pair], yerr=[error(r) for r in pair],
                    marker="o", capsize=4, label=label)
    ax.set(xlabel="LoRA rank", ylabel="Test macro-F1", xticks=[8, 16])
    ax.legend()
    save(fig, "rank.png")
    costs("pareto_memory.png", "peak_mib", "Peak allocated GPU memory (MiB)")
    costs("pareto_time.png", "train_seconds", "Training time (seconds)")

    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8), sharey=True)
    for ax, (model, model_label) in zip(axes, MODELS.items()):
        for method, label in METHODS.items():
            picked = lookup[(model, choices[model][method])]
            reduced = [r for r in rows if r["model"] == model and r["method"] == method
                       and r["experiment"] == "08"]
            series = sorted([*reduced, picked], key=lambda r: float(r["fraction"]))
            ax.errorbar([100*float(r["fraction"]) for r in series], [f1(r) for r in series],
                        yerr=[error(r) for r in series], capsize=3, marker="o",
                        color=COLORS[method], label=label)
        ax.set(title=model_label, xlabel="Training examples used (%)", xticks=[25, 50, 100])
    axes[0].set_ylabel("Test macro-F1")
    axes[-1].legend(fontsize=8)
    save(fig, "scarcity.png")

    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    for method, label in METHODS.items():
        points = []
        for model in MODELS:
            hub_id = "FacebookAI/xlm-roberta-base" if model == "xlm-roberta-base" else model
            r = lookup[(model, choices[model][method])]
            points.append((audit["tokenizers"]["models"][hub_id]["fertility"], f1(r), error(r)))
        x, y, sd = zip(*points)
        ax.errorbar(x, y, yerr=sd, marker="o", capsize=3, color=COLORS[method], label=label)
    ax.set(xlabel="Training subwords per whitespace word", ylabel="Test macro-F1",
           title="Validation-selected full-data runs")
    ax.legend()
    save(fig, "fertility.png")
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    plot_results(parser.parse_args().evidence)
