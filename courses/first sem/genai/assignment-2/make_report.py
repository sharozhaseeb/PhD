"""Build the Assignment 2 report (PDF) from the notebook's outputs.

Every number comes from outputs/results.json and every figure from outputs/figures/,
so nothing measured is typed by hand.

Usage (in Colab after running the notebook, or locally after downloading outputs/):
    pip install reportlab
    python make_report.py --outputs /content/drive/MyDrive/CS5004_A2/outputs

Before building, fill in the three settings just below.
"""
import argparse
import json
from pathlib import Path

import matplotlib
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

# ---------------- Fill these in before building ----------------
STUDENT_NAME = "Sharoz Haseeb"
ROLL = "26L-9005"
D = int(ROLL[-1])                     # 5
DRIVE_LINK = "https://drive.google.com/drive/folders/1IBZFYrzogtZQV4_HEjULJ3JuiAPQM0ft"
# After looking at the two 4x4 grids, write which schedule gave better samples: "cosine" or "linear".
BETTER_SCHEDULE = "linear"
# One short sentence describing what you see in the samples (edit after looking at them).
SAMPLE_OBSERVATION = ("its grid has a good mix of all three classes (four or five sandals, about seven bags, three "
                      "trousers) and the sandals' thin straps and high heels are drawn quite sharply, while the other grid "
                      "is dominated by large, over-bright bag-like shapes (only two sandals and two trousers), several of "
                      "them flat white blobs with little detail")
# Optional: one sentence about the misclassified photos, written after looking at them
# (e.g. "Both models confused a white mug photographed from above with a book."). Leave "" if there are none.
B2_ERROR_NOTE = ""
# How many of the 100 photos are augmented copies (files ending in _aug); 0 if all 100 are real phone photos.
N_AUGMENTED = 8
# ----------------------------------------------------------------

# DejaVu Sans ships with matplotlib and has the Greek letters and maths symbols we need.
FONT_DIR = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("DejaVu", str(FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold")

styles = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=styles["BodyText"], fontName="DejaVu", fontSize=9, leading=12)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8, leading=10)
H1 = ParagraphStyle("h1", parent=BODY, fontName="DejaVu-Bold", fontSize=13, leading=16, spaceBefore=6, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=BODY, fontName="DejaVu-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=3)
TITLE = ParagraphStyle("title", parent=H1, fontSize=15, alignment=1)
CENTER = ParagraphStyle("center", parent=BODY, alignment=1)

PAGE_W = A4[0] - 3 * cm                        # usable width (1.5 cm margins)


def p(text, style=BODY):
    return Paragraph(text, style)


def fig(path, width_frac=1.0, max_h=None):
    """A figure scaled to a fraction of the page width (keeps the aspect ratio)."""
    w, h = ImageReader(str(path)).getSize()
    width = PAGE_W * width_frac
    height = width * h / w
    if max_h and height > max_h:
        height, width = max_h, max_h * w / h
    return Image(str(path), width=width, height=height)


def sci(x):
    """1.5399e+11 -> '1.540 × 10^11' (as a reportlab superscript)."""
    mantissa, exponent = f"{x:.3e}".split("e")
    return f"{mantissa} × 10<super>{int(exponent)}</super>"


def table(rows, col_widths=None, font_size=8):
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
        ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dde5f0")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def build(out_dir: Path, pdf_path: Path):
    for name, value in [("STUDENT_NAME", STUDENT_NAME), ("DRIVE_LINK", DRIVE_LINK)]:
        if "PASTE" in value:
            raise SystemExit(f"Fill in {name} at the top of make_report.py before building the report.")
    R = json.loads((out_dir / "results.json").read_text())
    F = out_dir / "figures"
    s = []

    # ---------------- Title ----------------
    s += [p("CS5004 Advanced Topics in Generative AI — Assignment 2", TITLE),
          p(f"Diffusion Models, Vision Transformers and Swin<br/>{STUDENT_NAME} · {ROLL} · d = {D}", CENTER),
          Spacer(1, 4),
          p(f"<b>Personal settings (d = {D}):</b> Part A classes 5 Sandal, 8 Bag, 1 Trouser (18,000 training images); "
            f"Part C image {R['C']['H']} × {R['C']['H']} × 3 with C = {R['C']['C']}. "
            f"<b>Drive folder (Part A checkpoints and Part B photos):</b> "
            f'<link href="{DRIVE_LINK}" color="blue">{DRIVE_LINK}</link>. '
            f"<b>Setup:</b> Google Colab T4 GPU, seed 9005, PyTorch + diffusers (UNet2DModel only) + timm + scikit-learn.")]

    # ---------------- A1 ----------------
    a1 = R["A1"]
    lin, cos = a1["linear"], a1["cosine"]
    s += [p("Part A: A Small Diffusion Model from Scratch", H1),
          p("Fashion-MNIST images are padded from 28 × 28 to 32 × 32 and scaled to [−1, 1]. The network is a "
            "diffusers.UNet2DModel built from a configuration with random weights; the noise schedules, forward process, "
            "training loop and sampling loop are my own PyTorch code (no diffusers schedulers or pipelines). "
            "Timesteps are 0-indexed, t = 0 … 999."),
          p("A1. Forward process and noise schedules", H2),
          p("Linear: β<sub>t</sub> from 10<super>−4</super> to 0.02, T = 1000. Cosine (Nichol &amp; Dhariwal, 2021): "
            "ᾱ(t) = f(t)/f(0), f(t) = cos²(((t/T) + s)/(1 + s) · π/2), s = 0.008, β<sub>t</sub> = 1 − ᾱ(t+1)/ᾱ(t) clipped at "
            "0.999, and ᾱ<sub>t</sub> recomputed as the product of (1 − β). Forward process: "
            "x<sub>t</sub> = √ᾱ<sub>t</sub> x<sub>0</sub> + √(1 − ᾱ<sub>t</sub>) ε."),
          Table([[fig(F / "A1_alpha_bar.png", 0.42), fig(F / "A1_forward_grid.png", 0.56)]],
                colWidths=[PAGE_W * 0.43, PAGE_W * 0.57]),
          p(f"<b>Which schedule destroys the image faster?</b> The <b>linear</b> schedule: its ᾱ<sub>t</sub> drops below 0.5 at "
            f"t = {lin['first_t_below_0.5']} and below 0.01 at t = {lin['first_t_below_0.01']} (ᾱ<sub>500</sub> = "
            f"{lin['alpha_bar_at']['500']:.3f}), while the cosine schedule reaches 0.5 only at t = {cos['first_t_below_0.5']} "
            f"(ᾱ<sub>500</sub> = {cos['alpha_bar_at']['500']:.3f}) and 0.01 at t = {cos['first_t_below_0.01']}; in the grid "
            f"the object is barely visible at t = 500 under the linear schedule but still clear under the cosine one. "
            f"Because training samples t uniformly, with the linear schedule about "
            f"{round(100 * (1000 - lin['first_t_below_0.01']) / 1000)}% of the training steps see inputs that are "
            f"practically pure noise, where there is little to learn. The cosine schedule spreads the destruction more evenly over "
            f"the timesteps, so more of the training budget is spent on partly-noised images where the network learns useful "
            f"denoising, which matters especially for small 32 × 32 images.")]

    # ---------------- A2 ----------------
    a2 = R["A2"]
    rows = [["model", "epochs", "batch", "learning rate", "optimiser", "steps", "training time", "loss (last epoch)"]]
    for name in ["linear", "cosine"]:
        i = a2[name]
        rows.append([name, i["epochs"], i["batch_size"], f"{i['lr']:g}", "AdamW",
                     f"{i['steps']:,}", f"{i['train_time_s'] / 60:.1f} min", f"{i['final_loss_last_epoch']:.4f}"])
    s += [p("A2. Training with the ε-prediction loss", H2),
          p(f"U-Net: block_out_channels = (32, 64, 128), 2 layers per block, self-attention only at the 8 × 8 "
            f"resolution, {a2['linear']['unet_params']:,} parameters, random initialisation. Training step: sample a batch "
            f"x<sub>0</sub>, t ~ U{{0,…,999}} and ε ~ N(0, I), build x<sub>t</sub> with the closed form, predict "
            f"ε<sub>θ</sub>(x<sub>t</sub>, t) and minimise the MSE ‖ε − ε<sub>θ</sub>‖². Both models use identical settings "
            f"(same seed, U-Net, batch size, learning rate and epochs); the number of epochs was chosen by timing a few "
            f"steps so that each run takes about 15 minutes on a Colab T4. AdamW in float32; each epoch "
            f"is {a2['linear']['train_images']:,} // {a2['linear']['batch_size']} = "
            f"{a2['linear']['train_images'] // a2['linear']['batch_size']} full batches (the last partial batch is skipped). "
            f"Both checkpoints are saved in the Drive folder."),
          table(rows),
          Spacer(1, 3),
          fig(F / "A2_loss_curves.png", 0.62),
          p("The two loss values are not directly comparable: for the same t the schedules give different noise levels, "
            "and at very noisy timesteps (many more of them under the linear schedule) predicting ε is easy because "
            "x<sub>t</sub> ≈ ε. A lower average loss therefore does not mean better samples.", SMALL)]

    # ---------------- A3 ----------------
    a3 = R["A3"]
    if BETTER_SCHEDULE == "cosine":
        agree = ("This agrees with A1: the linear schedule wastes many training steps on almost pure noise, while the "
                 "cosine schedule spends the same budget on informative noise levels.")
    else:
        agree = ("This only partly agrees with A1. The trajectories confirm A1's point that the cosine schedule destroys "
                 "information more slowly: the cosine x̂<sub>0</sub> already has the object's outline at t ≈ 900, while the "
                 "linear x̂<sub>0</sub> is still noise there and a shape appears only around t ≈ 750–600. But that did not turn "
                 "into better samples: sandals are mostly thin straps, details decided in the last low-noise steps, and a "
                 "likely reason for the many bags in the cosine grid is that its model commits to a large bright shape very "
                 "early in sampling. With 16 samples and ~16 minutes of training this is a visual judgement, not a measurement.")
    s += [p("A3. Sampling with DDPM", H2),
          p("All 1000 reverse steps: x<sub>t−1</sub> = (1/√α<sub>t</sub>)(x<sub>t</sub> − (β<sub>t</sub>/√(1 − ᾱ<sub>t</sub>)) "
            "ε<sub>θ</sub>) + σ<sub>t</sub>z with σ<sub>t</sub>² = β<sub>t</sub>, starting from x<sub>999</sub> ~ N(0, I); "
            "no noise is added at the last step. At each step x̂<sub>0</sub> is clamped to [−1, 1] and the matching "
            "ε = (x<sub>t</sub> − √ᾱ<sub>t</sub> x̂<sub>0</sub>)/√(1 − ᾱ<sub>t</sub>) is used in the formula (as in the original DDPM "
            "code). Without it the cosine model fails: β<sub>999</sub> = 0.999 makes 1/√α<sub>999</sub> ≈ 31.6, so small ε errors "
            f"at t = 999 are amplified and grow until {a3.get('cosine_no_clip_black_fraction', 0):.0%} of the pixels end up "
            "black, while for the linear model (1/√α<sub>999</sub> ≈ 1.01) the unclipped samples differ from the clipped ones by "
            f"only {a3.get('linear_no_clip_mean_abs_diff', 0):.3f} per pixel on average (same seed). The reverse step is the "
            "handout formula itself (clip_x0=False runs it literally; this ablation is in the notebook). Sampling times (16 images, 1000 U-Net evaluations each batch): "
            f"linear {a3['linear']['sampling_time_s_for_16']:.1f} s, cosine {a3['cosine']['sampling_time_s_for_16']:.1f} s."),
          Table([[fig(F / "A3_samples_linear.png", 0.4), fig(F / "A3_samples_cosine.png", 0.4)]]),
          p("Denoising trajectory of one sample at 8 timesteps (top row x<sub>t</sub>, bottom row the predicted clean image "
            "x̂<sub>0</sub> = (x<sub>t</sub> − √(1 − ᾱ<sub>t</sub>) ε<sub>θ</sub>)/√ᾱ<sub>t</sub>, clamped to [−1, 1]):"),
          fig(F / "A3_trajectory_linear.png", 0.92),
          fig(F / "A3_trajectory_cosine.png", 0.92),
          p("At the first timesteps √ᾱ<sub>t</sub> ≈ 0, so x̂<sub>0</sub> divides a small error by a tiny number "
            "(1/√ᾱ<sub>999</sub> ≈ 157 linear, ≈ 20,000 cosine) and those panels are clamped noise. With 0-indexed steps the "
            "last panel is x<sub>t</sub> at t = 0, the input of the final step; the final sample looks the same.", SMALL),
          p(f"<b>Comparison.</b> Both models give recognisable sandals, bags and trousers. The <b>{BETTER_SCHEDULE}</b> "
            f"model's samples look better for my classes: {SAMPLE_OBSERVATION}. {agree} "
            f"<b>Why 1000 evaluations for sampling but one for training?</b> In training the closed form "
            f"q(x<sub>t</sub> | x<sub>0</sub>) jumps straight to a random t, and the loss at that one t is an unbiased term of "
            f"the full objective, so one forward pass per image suffices. In sampling x<sub>0</sub> is unknown and the reverse "
            f"process has no closed form: each x<sub>t−1</sub> depends on x<sub>t</sub>, which came from the previous network "
            f"output, so the 1000 steps form a sequential chain of 1000 U-Net evaluations that cannot be run in parallel.")]

    # ---------------- B ----------------
    b1, b2 = R["B1"], R["B2"]
    s += [PageBreak(),
          p("Part B: Inside ViT and Swin", H1),
          p(f"My own dataset: 4 classes ({', '.join(b2['classes'])}), 25 photos each, taken with my phone with different objects, "
            f"backgrounds, angles and lighting"
            + (f" ({100 - N_AUGMENTED} real photos; two accidental blurry shots were removed and the short classes were "
               f"topped up with {N_AUGMENTED} augmented copies (flip, small rotation, crop, brightness), which are used only "
               f"in the training split, so all test photos are real)" if N_AUGMENTED else "")
            + f". Photos are opened with ImageOps.exif_transpose and preprocessed only with each model's own timm "
            f"transform (resolve_model_data_config + create_transform, is_training=False: resize shorter side, centre-crop "
            f"224 × 224, normalise with that model's mean and std). Models: pretrained vit_base_patch16_224 and "
            f"swin_tiny_patch4_window7_224, no fine-tuning."),
          fig(F / "B_dataset_collage.png", 1.0),
          p("B1. Trace the shapes (forward hooks, one 224 × 224 image)", H2)]
    cols = ["module", "output shape", "tokens", "grid", "channels", "stride vs input", "downsampling here?"]
    for title, key in [("ViT-B/16", "vit_table"), ("Swin-T", "swin_table")]:
        rows = [cols] + [[str(r[c]) for c in cols] for r in b1[key]]
        s += [p(f"<b>{title}</b>", SMALL), table(rows, font_size=7.5), Spacer(1, 3)]
    s += [p(f"<b>Parameters:</b> ViT-B/16 {b1['vit_params']:,} ({b1['vit_params'] / 1e6:.1f} M); Swin-T "
            f"{b1['swin_params']:,} ({b1['swin_params'] / 1e6:.1f} M). ViT patchifies once (16 × 16 patches → 196 tokens, "
            f"plus [CLS] = 197) and then every block keeps 197 × 768. Swin starts with 4 × 4 patches (56 × 56 × 96); in timm "
            f"the Patch Merging layer at the start of stages 2, 3 and 4 halves the grid and doubles the channels, giving "
            f"strides 4, 8, 16, 32 (features_only=True returns exactly these four maps)."),
          p("<b>Why Swin can feed an FPN directly but ViT cannot.</b> An FPN needs a pyramid of feature maps at several "
            "resolutions, like ResNet's C2–C5, and Swin's four stages provide exactly that (56², 28², 14², 7² at 96–768 "
            "channels). ViT has one single-scale 14 × 14 × 768 map (stride 16) at every depth, so the pyramid would have to be "
            "built by extra up/down-sampling, and its global attention grows quadratically with image size, which is costly "
            "for the high-resolution images used in detection.")]

    nice = {"vit": "ViT-B/16", "swin": "Swin-T"}
    gap = b2["vit"]["n_wrong"] - b2["swin"]["n_wrong"]          # > 0 means Swin made fewer mistakes (same rule as notebook)
    if gap == 0:
        sure = min(["vit", "swin"], key=lambda k: b2[k]["test_log_loss"])
        other = "swin" if sure == "vit" else "vit"
        winner = sure
        verdict = (f"Both backbones made the same number of test errors ({b2['vit']['n_wrong']}/{b2['n_test']}), but "
                   f"<b>{nice[sure]}</b> was more confident in the right answers (test log-loss "
                   f"{b2[sure]['test_log_loss']:.3f} vs {b2[other]['test_log_loss']:.3f}, mean probability of the true "
                   f"class {b2[sure]['mean_prob_true_class']:.3f} vs {b2[other]['mean_prob_true_class']:.3f}).")
        if b2[other]["test_log_loss"] - b2[sure]["test_log_loss"] < 0.01:
            verdict += " That gap is tiny, so on my photos the two backbones are effectively equally good."
        else:
            verdict += f" So {nice[sure]}'s features separate my classes slightly better."
    else:
        winner, loser = ("swin", "vit") if gap > 0 else ("vit", "swin")
        verdict = (f"<b>{nice[winner]}</b> gave the better features on my photos: {b2[winner]['n_wrong']} vs "
                   f"{b2[loser]['n_wrong']} wrong out of {b2['n_test']} (macro-F1 {b2[winner]['macro_f1']:.3f} vs "
                   f"{b2[loser]['macro_f1']:.3f}).")
        if abs(gap) <= 2:
            verdict += (" The gap is only one or two photos (one error = 3.3% accuracy), so it is small and could change "
                        "with a different split.")
    rows = [["backbone", "feature", "accuracy", "macro-F1", "misclassified", "test log-loss", "mean p(true)"]]
    for k, feat in [("vit", "[CLS] token (768)"), ("swin", "global avg pool (768)")]:
        rows.append([nice[k], feat, f"{b2[k]['accuracy']:.3f}", f"{b2[k]['macro_f1']:.3f}",
                     f"{b2[k]['n_wrong']} / {b2['n_test']}", f"{b2[k]['test_log_loss']:.3f}",
                     f"{b2[k]['mean_prob_true_class']:.3f}"])
    why = {
        "swin": ("Swin builds features hierarchically with local window attention, so its final map mixes fine local detail "
                 "with the overall shape, and global average pooling summarises all 49 positions, which is robust when the "
                 "object is off-centre or the background changes."),
        "vit": ("ViT-B/16 is about three times larger and its timm weights were pre-trained on ImageNet-21k before "
                "ImageNet-1k fine-tuning, so its [CLS] token carries very general, semantic information that separates my "
                "everyday-object classes well."),
    }
    near_tie = gap == 0 and abs(b2["vit"]["test_log_loss"] - b2["swin"]["test_log_loss"]) < 0.01
    reason = (why["vit"] + " " + why["swin"] + " Both strengths matter for photos of distinct everyday objects, "
              "so both probes separate my four classes perfectly.") if near_tie else why[winner]
    n_wrong = b2["vit"]["n_wrong"] + b2["swin"]["n_wrong"]
    if n_wrong == 0:
        errors = "Neither probe misclassified any of the 30 test photos, so there are no misclassified images to show."
    else:
        errors = B2_ERROR_NOTE or "The confusion matrices and the misclassified photos above show which classes get mixed up."
    wrong_fig = ([fig(F / "B2_misclassified.png", 0.62, max_h=7.5 * cm)] if n_wrong else [])
    s += [PageBreak(),
          p("B2. Linear probe on my photos", H2),
          p(f"Both backbones are frozen. One feature per image ([CLS] token for ViT, global average pooling of the final "
            f"7 × 7 × 768 map for Swin) is standardised and fed to a logistic-regression classifier. The same stratified "
            f"70/30 split is used for both ({b2['n_train']} train / {b2['n_test']} test photos)."),
          table(rows),
          Spacer(1, 3),
          fig(F / "B2_confusion_matrices.png", 0.8),
          *wrong_fig,
          p(f"<b>Discussion.</b> {verdict} {reason} {errors}")]

    # ---------------- C ----------------
    c = R["C"]
    H, hw, C = c["H"], c["hw"], c["C"]
    sides = [H // 4 // 2 ** i for i in range(4)]          # h = w at stages 1..4
    chans = [C * 2 ** i for i in range(4)]
    wins = [(sd // 7) ** 2 for sd in sides]
    rows = [["layer", "output (h × w × c)", "windows (h/M)²"]] + [[r["layer"], r["output (h×w×c)"], r["windows"]] for r in c["table"]]
    s += [PageBreak(),
          p(f"Part C: Swin dimensions and attention cost by hand (d = {D})", H1),
          p(f"Settings: H × W × 3 = {H} × {H} × 3, C = {C}, patch size 4, window M = 7, depths 2, 2, 6, 2."),
          p(f"<b>1. Output sizes.</b> Patch partition + linear embedding: {H}/4 = {sides[0]}, so each 4 × 4 × 3 = 48-value "
            f"patch is projected to C = {C} → {sides[0]} × {sides[0]} × {C}. Stage 1 (2 blocks, no merging) keeps "
            f"{sides[0]} × {sides[0]} × {C}. Each later stage starts with patch merging (concatenate 2 × 2 neighbours → 4C, "
            f"linear layer → 2C), halving h and w and doubling the channels: "
            + "; ".join(f"stage {i + 1}: {sides[i - 1]}/2 = {sides[i]} → {sides[i]} × {sides[i]} × {chans[i]}"
                        for i in range(1, 4)) + "."),
          p("<b>2. Windows.</b> Non-overlapping 7 × 7 windows: "
            + "; ".join(f"stage {i + 1} ({sides[i]}/7)² = {sides[i] // 7}² = {wins[i]}" for i in range(4))
            + ". Every size divides by 7, so no padding is needed; each window holds M² = 49 tokens."),
          table(rows, col_widths=[PAGE_W * 0.35, PAGE_W * 0.3, PAGE_W * 0.3]),
          Spacer(1, 4),
          p(f"<b>3. Attention cost, one stage-1 layer</b> (h = w = {sides[0]}, hw = {sides[0]}² = {hw:,}, C = {C}, "
            f"C² = {C * C:,}, M² = 49):"),
          p(f"Ω(MSA) = 4hwC² + 2(hw)²C = 4 × {hw:,} × {C * C:,} + 2 × {hw:,}² × {C} "
            f"= {4 * hw * C * C:,} + 2 × {hw * hw:,} × {C} = {4 * hw * C * C:,} + {2 * hw * hw * C:,} "
            f"= <b>{c['omega_msa']:,}</b> ≈ {sci(c['omega_msa'])}"),
          p(f"Ω(W-MSA) = 4hwC² + 2M²hwC = {4 * hw * C * C:,} + 2 × 49 × {hw:,} × {C} = {4 * hw * C * C:,} + "
            f"{2 * 49 * hw * C:,} = <b>{c['omega_wmsa']:,}</b> ≈ {sci(c['omega_wmsa'])}"),
          p(f"<b>Ratio</b> Ω(MSA)/Ω(W-MSA) = {c['omega_msa']:,} / {c['omega_wmsa']:,} ≈ <b>{c['ratio']:.2f}</b>. "
            f"Check: dividing both by 2hwC gives (2C + hw)/(2C + M²) = ({2 * C} + {hw:,})/({2 * C} + 49) = "
            f"{2 * C + hw:,}/{2 * C + 49} ≈ {(2 * C + hw) / (2 * C + 49):.2f}. Global attention in stage 1 would cost about "
            f"{round(c['ratio'])} times more; the (hw)² term, quadratic in the number of tokens, dominates MSA "
            f"({2 * hw * hw * C / c['omega_msa']:.1%} of its cost), while W-MSA is linear in hw. Comparing only the attention "
            f"terms, 2(hw)²C / 2M²hwC = hw/M² = {hw // 49} = the number of stage-1 windows; the shared 4hwC² projection "
            f"term is why the full ratio is smaller.")]

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                            topMargin=1.3 * cm, bottomMargin=1.3 * cm,
                            title=f"{ROLL} CS5004 Assignment 2", author=STUDENT_NAME)
    page_count = []
    doc.build(s, onLaterPages=lambda c, d: page_count.append(d.page), onFirstPage=lambda c, d: page_count.append(d.page))
    pages = max(page_count)
    print(f"wrote {pdf_path} ({pages} pages)")
    if pages > 8:
        print("WARNING: the report must be at most 8 pages")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", default="A2_work/outputs", help="folder with results.json and figures/")
    ap.add_argument("--pdf", default=None, help="output PDF path (default: <outputs>/<ROLL>_A2_report.pdf)")
    args = ap.parse_args()
    out = Path(args.outputs)
    build(out, Path(args.pdf) if args.pdf else out / f"{ROLL}_A2_report.pdf")
