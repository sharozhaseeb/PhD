"""Build a six-page report from a complete, verified evidence directory."""

import argparse
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (Image as PDFImage, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)
from xml.sax.saxutils import escape

from collect_results import HERE, load
from make_figures import MODELS, METHODS, plot_results

NAVY = colors.HexColor("#183752")
PALE = colors.HexColor("#ebf3f8")


def number(row, field, digits):
    return f"{float(row[field+'_mean']):.{digits}f} ± {float(row[field+'_sd']):.{digits}f}"


def build(root, contribution, output):
    rows = plot_results(root)  # Raises if any of the 64 real runs is missing.
    audit = load(HERE / "track3_preflight.json")
    selection = load(root / "validation_selection.json")["choices"]
    full = [r for r in rows if r["experiment"] != "08"]
    lookup = {(r["model"], r["experiment"]): r for r in full}
    w, h = A4
    width = w - 94
    story = []
    body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.7, leading=14, textColor=NAVY)
    title = ParagraphStyle("title", parent=body, fontName="Helvetica-Bold", fontSize=19, leading=23,
                           spaceAfter=12)
    caption = ParagraphStyle("caption", parent=body, fontSize=8.3, leading=11)

    def para(text, style=body):
        story.append(Paragraph(escape(text), style))
        story.append(Spacer(1, 7))

    def page(heading):
        if story:
            story.append(PageBreak())
        para(heading, title)

    def table(data, widths=None, padding=6):
        t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), padding),
            ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ]))
        story.extend([t, Spacer(1, 12)])

    def figure(name, caption_text):
        path = root / "figures" / name
        with Image.open(path) as image:
            ratio = image.width / image.height
        fw = min(width, 296 * ratio)
        story.append(PDFImage(str(path), width=fw, height=fw/ratio))
        para(caption_text, caption)

    page("Urdu sentiment: fine-tuning at lower cost")
    para("Advanced Generative AI Assignment 3 | Track 3 | Group 3 | 26L-9005 | Seeds 3 and 103")
    para("Two pretrained encoders classify Positive, Negative and Objective tweets.")
    table([["Split", "Total", "Positive", "Negative", "Objective"]] + [
        [key.title(), val["count"], *[val["labels"][k] for k in ("Positive", "Negative", "Objective")]]
        for key, val in audit["splits"].items()])
    table([
        ["Setting", "Value"],
        ["Encoders", "XLM-R base and MuRIL base cased"],
        ["Dataset", "Urdu Sentiment Corpus v1, pinned author TSV, 1,000 raw rows"],
        ["Text normalization", "Remove URLs and mentions, unify yeh and kaf, collapse whitespace"],
        ["Row filtering", "Reject empty or invalid rows and deduplicate normalized text"],
        ["Rows removed", "One invalid row, one duplicate, two rows with conflicting labels"],
        ["Splits", "996 rows, stratified 70/15/15 with seed 3, fixed for all runs"],
        ["Training", "3 epochs, effective batch 16, final epoch, T4 FP16"],
        ["Batching", "Microbatch 8, accumulation 2, evaluation batch 16"],
        ["Learning rates", "2e-5 for Full FT and 2e-4 for PEFT, with linear decay"],
        ["Other settings", "No warmup or weight decay, gradient clipping at 1.0"],
        ["Sequence length", "43, the larger training p95, with dynamic padding"],
        ["LoRA / QLoRA", "Rank 8/16, alpha 16, dropout 0, no adapter bias updates"],
        ["PEFT classifier", "The classification head is trainable in every run"],
        ["LoRA placement", "Query and value, with FFN output added in experiment 04"],
        ["QLoRA", "NF4 with double quantization and FP16 compute, rank 16"],
        ["IA3", "Key/value with or without FFN output projection"],
        ["Optimizer", "AdamW, with 32-bit bitsandbytes paged/unpaged for QLoRA"],
    ], padding=4)
    data = [["Tokenizer", "Fertility", "p95", "Truncated", "UNK rate"]]
    for model, r in audit["tokenizers"]["models"].items():
        data.append(["MuRIL" if "muril" in model else "XLM-R", f"{r['fertility']:.3f}",
                     r["p95_nearest_rank"], f"{r['truncation_rate']:.2%}", f"{r['unknown_rate']:.3%}"])
    table(data)
    para("Tokenizer measurements use the same training texts. Fertility and UNK exclude special tokens; length and truncation include them. Memory is peak PyTorch CUDA allocation, measured over training only.")

    headings = ["Model / run", "Method", "F1", "Accuracy", "Sec.", "MiB", "Trainable"]

    def metrics_table(population, scarcity=False):
        values = [headings]
        for row in population:
            tag = f"{float(row['fraction']):.0%}/{row['effective_experiment']}" if scarcity else row["experiment"]
            values.append([MODELS[row["model"]] + " " + tag, METHODS[row["method"]],
                           number(row, "macro_f1", 3), number(row, "accuracy", 3),
                           number(row, "train_seconds", 1), number(row, "peak_mib", 0),
                           number(row, "trainable_params", 0)])
        table(values, [90, 58, 69, 69, 67, 66, 82])

    page("Full-data comparison")
    para("Held-out accuracy and macro-F1; all metrics are mean ± sample SD for seeds 3 and 103. MiB is allocated GPU memory, not total memory reserved.")
    metrics_table(full)
    para("01 Full FT; 02/03 LoRA rank 8/16; 04 adds FFN placement; 05/06 QLoRA paging on/off; 07a/07b IA3 attention only/attention + FFN.", caption)

    page("Reduced-data comparison")
    para("Each encoder and method uses the highest mean validation macro-F1, with ties resolved by the first experiment. The row tag shows the fraction and source configuration. Its 100% value comes from page 2. Both IA3 selections, both QLoRA selections and MuRIL LoRA were ties.")
    metrics_table([r for r in rows if r["experiment"] == "08"], scarcity=True)
    para("The two seeds use paired, nested 25% and 50% subsets. Variation includes subset composition on the reduced runs.", caption)

    page("Rank and GPU memory")
    figure("rank.png", "Figure 1. LoRA rank comparison at fixed alpha=16, so the update scaling also changes.")
    figure("pareto_memory.png", "Figure 2. Macro-F1 versus peak GPU allocation. Circles show XLM-R and squares show MuRIL. Faded points use 25% or 50% of training data.")

    page("Time and label scarcity")
    figure("pareto_time.png", "Figure 3. Macro-F1 versus synchronized training time across all data fractions.")
    figure("scarcity.png", "Figure 4. Label scarcity for the validation-selected configurations, compared with their own full-data runs.")

    page("Tokenizer comparison and discussion")
    figure("fertility.png", "Figure 5. Fertility and macro-F1 for each method's selected configuration on the two encoders.")
    xlmr = {exp: lookup[("xlm-roberta-base", exp)] for exp in ("01", "04", "05", "06")}
    def profile(row):
        return (f"{float(row['macro_f1_mean']):.3f} F1, "
                f"{float(row['peak_mib_mean']):,.0f} MiB, {float(row['train_seconds_mean']):.1f} s")
    baseline, paged = xlmr["01"], xlmr["05"]
    memory_saved = float(baseline["peak_mib_mean"]) - float(paged["peak_mib_mean"])
    f1_lost = float(baseline["macro_f1_mean"]) - float(paged["macro_f1_mean"])
    extra_time = float(paged["train_seconds_mean"]) - float(baseline["train_seconds_mean"])
    para(f"RQ1. On full-data XLM-R, Full FT scored highest ({profile(baseline)}). Paged QLoRA saved {memory_saved:,.0f} MiB ({memory_saved / float(baseline['peak_mib_mean']):.0%}), lost {f1_lost:.3f} F1 and took {extra_time:.1f} s longer. FFN LoRA ({profile(xlmr['04'])}) reduced both memory and time versus Full FT. Both QLoRA variants gave the same F1 on each encoder, with minimal allocation differences.")
    for model, label in MODELS.items():
        f = lambda exp: float(lookup[(model, exp)]["macro_f1_mean"])
        m = lambda exp: float(lookup[(model, exp)]["peak_mib_mean"])
        picked = selection[model]
        drops = {
            r["method"]: f(picked[r["method"]]) - float(r["macro_f1_mean"])
            for r in rows if r["model"] == model and r["experiment"] == "08" and float(r["fraction"]) == 0.25
        }
        para(f"{label} rank 16 changes F1 by {f('03')-f('02'):+.3f} versus rank 8, with more trainable weights. FFN placement changes F1 by {f('04')-f('03'):+.3f} for LoRA and {f('07b')-f('07a'):+.3f} for IA3. Paged QLoRA changes F1 by {f('05')-f('03'):+.3f} and allocation by {m('05')-m('03'):+.0f} MiB versus rank-16 attention LoRA.")
        if label == "XLM-R":
            robust = min(drops, key=drops.get)
            para("RQ3. XLM-R 25% minus 100% F1 changes were " + ", ".join(
                f"{METHODS[method]} {-drop:+.3f}" for method, drop in drops.items())
                + f". {METHODS[robust]} retained the most F1 by this measure. MuRIL's majority-class baseline makes its small, non-monotonic changes hard to interpret.")
    para("RQ2. MuRIL used fewer subwords per word (1.313 vs 1.401) and produced more unknown tokens (2.196% vs 0.006%). Every full-data MuRIL model predicted Negative throughout the test set (0.222 macro-F1, 0.500 accuracy). All 64 runs missed Objective (3 test examples, F1 = 0). Encoder architecture and pretraining also differ. Two seeds give a descriptive spread.")
    para("The measured QLoRA rows use the corrected 2e-4 learning rate. Three XLM-R runs flagged one nonfinite gradient norm each. The logs preserve these flags and the runs completed all epochs with finite final parameters.", caption)
    para("Contribution: " + contribution)

    def foot(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(NAVY)
        canvas.drawString(47, 28, "Advanced GenAI | Assignment 3")
        canvas.drawRightString(w - 47, 28, str(doc.page))

    SimpleDocTemplate(str(output), pagesize=A4, topMargin=49, bottomMargin=45,
                      leftMargin=47, rightMargin=47, title="Assignment 3: Urdu sentiment").build(
                          story, onFirstPage=foot, onLaterPages=foot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--contribution", required=True, help="Truthful short member contribution statement")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.evidence, args.contribution, args.output)
