"""Concept diagrams for the slow walkthrough videos (saved to diagrams/)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = Path(__file__).parent / "diagrams"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "Segoe UI", "font.size": 15})
BLUE, ORANGE, GREEN, GREY, RED, PURPLE = "#2f6db5", "#e08a1e", "#2e8b57", "#9a9a9a", "#c0392b", "#7d5ba6"
LIGHT = {BLUE: "#dce8f7", ORANGE: "#fbe7cc", GREEN: "#d8efe1", GREY: "#ececec", RED: "#f6d5d1", PURPLE: "#e7def2"}


def canvas(title):
    fig, ax = plt.subplots(figsize=(12.4, 8.6), dpi=100)
    ax.set_xlim(0, 124)
    ax.set_ylim(0, 86)
    ax.axis("off")
    ax.text(62, 82, title, ha="center", va="center", fontsize=22, weight="bold", color="#222")
    return fig, ax


def box(ax, x, y, w, h, text, color=BLUE, fs=15, weight="normal", fill=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc=fill or LIGHT[color], ec=color, lw=2.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight, color="#222")


def arrow(ax, x0, y0, x1, y1, color="#444", text=None, fs=13, style="-|>", ls="-", tdx=0, tdy=1.6):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=20, lw=2, color=color, ls=ls))
    if text:
        ax.text((x0 + x1) / 2 + tdx, (y0 + y1) / 2 + tdy, text, ha="center", fontsize=fs, color=color)


def note(ax, x, y, text, color="#333", fs=14, ha="left", **kw):
    ax.text(x, y, text, ha=ha, va="top", fontsize=fs, color=color, linespacing=1.5, **kw)


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white", pad_inches=0.3)
    plt.close(fig)


def noisy(ax, x, y, s, level, seed=0):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:32, 0:32]
    img = ((np.abs(xx - 16) < 9) & (np.abs(yy - 17) < 8)).astype(float) * 1.6 - 0.8
    img[(yy > 6) & (yy < 10) & (np.abs(xx - 16) < 5) & (np.abs(xx - 16) > 2)] = 0.8   # bag handle
    ab = 1 - level
    img = np.sqrt(ab) * img + np.sqrt(1 - ab) * rng.standard_normal(img.shape)
    ax.imshow(img, cmap="gray", vmin=-1.5, vmax=1.5, extent=(x, x + s, y, y + s), zorder=3)


# ------------------------------------------------------------------ A2 diagrams
def ddpm_chain():
    fig, ax = canvas("DDPM: add noise step by step, then learn to remove it")
    xs = [6, 30, 54, 78, 102]
    labels = ["x0  (clean)", "x1", "x_t", "x_(T-1)", "x_T  (pure noise)"]
    levels = [0, 0.15, 0.5, 0.93, 1.0]
    for i, (x, lab, lv) in enumerate(zip(xs, labels, levels)):
        noisy(ax, x, 40, 16, lv, seed=i)
        ax.text(x + 8, 37, lab, ha="center", fontsize=15, weight="bold")
    for a, b in zip(xs[:-1], xs[1:]):
        arrow(ax, a + 17, 62, b - 1, 62, ORANGE)
        arrow(ax, b - 1, 33, a + 17, 33, BLUE)
    note(ax, 62, 72, "FORWARD  q(x_t | x_(t-1)): add a little Gaussian noise (variance beta_t). Fixed, no learning.", ORANGE, 15, "center")
    note(ax, 62, 29, "REVERSE  p_theta(x_(t-1) | x_t): the U-Net predicts the noise eps_theta and we remove a bit of it.", BLUE, 15, "center")
    box(ax, 8, 4, 50, 14, "Shortcut (closed form):\nx_t = sqrt(alpha_bar_t) * x0 + sqrt(1 - alpha_bar_t) * eps\njump from x0 to ANY step t in one go", ORANGE, 14)
    box(ax, 66, 4, 50, 14, "Training: pick random t, make x_t with the shortcut,\nask the U-Net to guess eps.\nLoss = mean squared error ( eps - eps_theta )", BLUE, 14)
    save(fig, "ddpm_chain.png")


def x0hat_clipping():
    fig, ax = canvas("One sampling step with $\hat{x}_0$ clipping (hat = 'our estimate')")
    box(ax, 2, 50, 18, 16, "x_t\n(current noisy\nimage)", GREY)
    box(ax, 26, 50, 18, 16, "U-Net\npredicts\neps_theta", BLUE)
    box(ax, 50, 50, 22, 16, "$\hat{x}_0$ = (x_t − sqrt(1−ᾱt)·eps_theta)\n / sqrt(ᾱt)\nguess of clean image", PURPLE, 13)
    box(ax, 78, 50, 18, 16, "clamp $\hat{x}_0$\nto [−1, 1]\n(valid pixels)", GREEN)
    box(ax, 102, 50, 20, 16, "recompute eps\nfrom clamped $\hat{x}_0$,\nthen DDPM step\n→ x_(t−1)", ORANGE, 13)
    for a, b in [(20.8, 25.2), (44.8, 49.2), (72.8, 77.2), (96.8, 101.2)]:
        arrow(ax, a, 58, b, 58)
    arrow(ax, 112, 49, 112, 38, ORANGE)
    arrow(ax, 112, 30, 11, 30, GREY, "repeat for t = 999, 998, …, 0   (no extra noise added at t = 0)", 14, tdy=1.4)
    arrow(ax, 11, 30, 11, 49, GREY)
    box(ax, 6, 4, 112, 17, "Why clip?  Cosine schedule: beta_999 = 0.999, so alpha_999 = 0.001 and 1/sqrt(alpha_999) ≈ 31.6.\n"
        "A tiny error in eps_theta at t = 999 is multiplied by ~31 and pixels explode → black images.\n"
        "Clamping the estimate $\hat{x}_0$ keeps every step inside the valid pixel range (same idea as clip_denoised in the DDPM code).", RED, 14)
    save(fig, "x0hat_clipping.png")


def vit_tokens():
    fig, ax = canvas("ViT-B/16: an image becomes a sequence of 197 tokens")
    # image grid
    ax.add_patch(Rectangle((4, 30), 32, 32, fc="#f3efe6", ec="#333", lw=2))
    for k in range(1, 14):
        ax.plot([4 + k * 32 / 14] * 2, [30, 62], color="#bbb", lw=0.8)
        ax.plot([4, 36], [30 + k * 32 / 14] * 2, color="#bbb", lw=0.8)
    ax.add_patch(Rectangle((4, 62 - 32 / 14), 32 / 14, 32 / 14, fc=ORANGE, ec="none"))
    note(ax, 20, 28, "224 × 224 photo\ncut into 16 × 16 patches\n→ 14 × 14 = 196 patches", "#333", 14, "center")
    arrow(ax, 38, 46, 47, 46, text="flatten +\nlinear layer", tdy=2)
    # tokens
    for i in range(9):
        c = GREEN if i == 0 else BLUE
        ax.add_patch(Rectangle((49 + i * 3.6, 36), 3, 20, fc=LIGHT[c], ec=c, lw=1.5))
    ax.text(49 + 1.5, 57.5, "[CLS]", ha="center", fontsize=12, color=GREEN, weight="bold")
    ax.text(68, 32, "1 [CLS] + 196 patch tokens = 197 tokens,\neach a vector of 768 numbers  (+ position embedding)", ha="center", fontsize=14, va="top")
    arrow(ax, 82, 46, 90, 46)
    box(ax, 91, 36, 30, 20, "12 transformer blocks\n(self-attention: every\ntoken looks at every\nother token)", BLUE, 14)
    box(ax, 4, 3, 117, 15, "Shape stays (197, 768) in every block: no downsampling, one resolution (patch size 16).\n"
        "For the linear probe we take the final [CLS] vector (768 numbers) as the image's feature.\n"
        "ViT-B/16 ≈ 86.6 M parameters; normalisation mean = std = 0.5 (from timm's config).", GREY, 14)
    save(fig, "vit_tokens.png")


def swin_stages():
    fig, ax = canvas("Swin-T: local windows, shifted windows, and a pyramid of stages")
    sizes = [(56, 96), (28, 192), (14, 384), (7, 768)]
    x = 4
    for k, (s, c) in enumerate(sizes):
        w = 18 - k * 3.5
        ax.add_patch(Rectangle((x, 36), w, w, fc=LIGHT[BLUE], ec=BLUE, lw=2))
        n = max(1, s // 7)
        if n > 1:
            for j in range(1, min(n, 8)):
                ax.plot([x + j * w / min(n, 8)] * 2, [36, 36 + w], color=BLUE, lw=0.6, alpha=0.6)
                ax.plot([x, x + w], [36 + j * w / min(n, 8)] * 2, color=BLUE, lw=0.6, alpha=0.6)
        ax.text(x + w / 2, 33, f"Stage {k + 1}\n{s} × {s} tokens\nC = {c}", ha="center", va="top", fontsize=13)
        if k < 3:
            arrow(ax, x + w + 1, 36 + w / 2, x + w + 8, 36 + (w - 3.5) / 2, ORANGE, "patch\nmerging", 11, tdy=1)
        x += w + 9
    note(ax, 4, 70, "224×224 image → 4×4 patches → 56×56 tokens. Each stage halves the grid and doubles channels (like a CNN).", "#333", 14)
    # window illustration
    ax.add_patch(Rectangle((92, 38), 14, 14, fc="white", ec="#333", lw=1.5))
    for j in (1,):
        ax.plot([99, 99], [38, 52], color=GREEN, lw=2.5)
        ax.plot([92, 106], [45, 45], color=GREEN, lw=2.5)
    ax.add_patch(Rectangle((108, 38), 14, 14, fc="white", ec="#333", lw=1.5))
    ax.plot([111.5, 111.5], [38, 52], color=PURPLE, lw=2.5)
    ax.plot([118.5, 118.5], [38, 52], color=PURPLE, lw=2.5)
    ax.plot([108, 122], [41.5, 41.5], color=PURPLE, lw=2.5)
    ax.plot([108, 122], [48.5, 48.5], color=PURPLE, lw=2.5)
    ax.text(97, 54, "W-MSA:\n7×7 windows", ha="center", fontsize=12, color=GREEN)
    ax.text(117.5, 54, "SW-MSA: shifted\nby 3 (none in stage 4)", ha="center", fontsize=12, color=PURPLE)
    box(ax, 4, 2, 117, 15, "Attention only inside each 7 × 7 window (M = 7) → cost grows linearly with image size, not quadratically.\n"
        "Next block shifts the windows so neighbouring windows can exchange information.\n"
        "Our hooks: stages (B, 56, 56, 96) → (B, 7, 7, 768); feature = global average pool of the last stage (768).", GREY, 14)
    save(fig, "swin_stages.png")


def linear_probe():
    fig, ax = canvas("Linear probe: frozen backbone + one simple classifier")
    box(ax, 2, 44, 16, 18, "your photo\n(224 × 224)", GREY)
    box(ax, 24, 40, 26, 26, "pretrained ViT / Swin\nFROZEN\n(no weights change)", BLUE, 15, "bold")
    box(ax, 56, 44, 18, 18, "feature\nvector\n768 numbers", PURPLE)
    box(ax, 80, 44, 16, 18, "Standard-\nScaler\n(mean 0, std 1)", GREY, 14)
    box(ax, 102, 44, 20, 18, "Logistic\nRegression\n→ class", GREEN, 15, "bold")
    for a, b in [(18.8, 23.2), (50.8, 55.2), (74.8, 79.2), (96.8, 101.2)]:
        arrow(ax, a, 53, b, 53)
    note(ax, 37, 36, "ViT: [CLS] token\nSwin: average pool", BLUE, 13, "center")
    box(ax, 4, 4, 117, 22, "Why a probe?  It measures how good the pretrained FEATURES are, with almost no training\n"
        "(only 768 × 4 weights + 4 biases are learned). Same split (70 / 30, stratified) for both models → fair comparison.\n"
        "Metrics: accuracy, macro-F1 (average F1 over classes), and log-loss (how confident the correct\n"
        "probabilities are; lower is better) – used as the tie-break when both models get 30 / 30.", GREY, 14)
    save(fig, "linear_probe.png")


# ------------------------------------------------------------------ A3 diagrams
def matrix(ax, x, y, w, h, color, label, sub=None, fs=15, hatch=None):
    ax.add_patch(Rectangle((x, y), w, h, fc=LIGHT[color], ec=color, lw=2.2, hatch=hatch))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, weight="bold")
    if sub:
        ax.text(x + w / 2, y - 1.5, sub, ha="center", va="top", fontsize=12, color="#444")


def finetune_vs_peft():
    fig, ax = canvas("Full fine-tuning vs parameter-efficient fine-tuning (PEFT)")
    ax.text(31, 74, "Full fine-tuning", ha="center", fontsize=18, weight="bold", color=RED)
    ax.text(93, 74, "PEFT (LoRA / QLoRA / IA3)", ha="center", fontsize=18, weight="bold", color=GREEN)
    for k in range(4):
        matrix(ax, 14, 58 - k * 11, 34, 8, RED, f"layer {k + 1} weights: TRAINED", fs=13)
        matrix(ax, 72, 58 - k * 11, 30, 8, GREY, f"layer {k + 1}: frozen", fs=13)
        matrix(ax, 104, 58 - k * 11, 8, 8, GREEN, "+", fs=16)
    note(ax, 31, 20, "all ≈ 278 M weights of XLM-R base get gradients\n+ Adam keeps 2 extra copies → most GPU memory\n(our run: 4,997 MiB peak)", RED, 14, "center")
    note(ax, 93, 20, "pretrained weights frozen; only a small add-on\n(green) + the classifier head are trained\n(e.g. LoRA r = 8: 887,811 trainable)", GREEN, 14, "center")
    save(fig, "finetune_vs_peft.png")


def lora():
    fig, ax = canvas("LoRA: keep W0 frozen, learn a small low-rank update B·A")
    matrix(ax, 3, 30, 6, 22, GREY, "x", "input\n(k = 768)")
    # main (frozen) path
    matrix(ax, 22, 26, 26, 22, GREY, "W0  frozen\n768 × 768", "pretrained weight (d × k)")
    arrow(ax, 9.5, 37, 21.5, 37)
    arrow(ax, 48.5, 37, 100.6, 37)
    # low-rank side path
    matrix(ax, 22, 58, 26, 9, ORANGE, "A:  r × k = 8 × 768", None, fs=14)
    ax.text(35, 69, "random init", ha="center", fontsize=12, color="#444")
    matrix(ax, 62, 58, 26, 9, GREEN, "B:  d × r = 768 × 8", None, fs=14)
    ax.text(75, 69, "zeros at start", ha="center", fontsize=12, color="#444")
    arrow(ax, 9.5, 46, 21.5, 62)
    arrow(ax, 48.5, 62.5, 61.5, 62.5, ORANGE, "only r = 8\nnumbers", 12, tdy=1.2)
    arrow(ax, 88.5, 62.5, 101.5, 39.5, GREEN, "× α/r", 14, tdx=4, tdy=0)
    ax.add_patch(plt.Circle((104, 37), 3.2, fc="white", ec="#333", lw=2))
    ax.text(104, 37, "+", ha="center", va="center", fontsize=22)
    arrow(ax, 107.4, 37, 117, 37)
    ax.text(118.5, 37, "h", fontsize=20, va="center", weight="bold")
    box(ax, 4, 1, 116, 15, "h = W0·x + (α / r)·B·A·x      ΔW = B·A has rank ≤ r  (\"low rank\" = few independent directions)\n"
        "Per matrix: r·(d + k) = 8 × (768 + 768) = 12,288 trainable instead of 768 × 768 = 589,824 (about 2%)\n"
        "Ours: query + value in 12 layers → 24 × 12,288 = 294,912; + classifier head 592,899 = 887,811\n"
        "α = 16, dropout 0.  B = 0 at start, so step 0 is exactly the pretrained model.", GREY, 13)
    save(fig, "lora.png")


def lora_where():
    fig, ax = canvas("Where the adapters sit inside one XLM-R layer (× 12 layers)")
    box(ax, 4, 58, 20, 10, "token vectors\n(768 each)", GREY, 14)
    for i, (n, c) in enumerate([("query", ORANGE), ("key", GREY), ("value", ORANGE)]):
        box(ax, 32 + i * 18, 58, 14, 10, n, c, 15, "bold" if c == ORANGE else "normal")
    box(ax, 88, 58, 30, 10, "attention → output.dense", GREY, 14)
    box(ax, 32, 36, 32, 10, "FFN intermediate\n768 → 3072", GREY, 13)
    box(ax, 70, 36, 32, 10, "FFN output.dense\n3072 → 768", PURPLE, 13, "bold")
    box(ax, 32, 16, 50, 10, "classifier head\n(modules_to_save → fully trained)", GREEN, 13, "bold")
    arrow(ax, 24.8, 63, 31.2, 63)
    arrow(ax, 103, 57, 48, 47)
    arrow(ax, 64.8, 41, 69.2, 41)
    arrow(ax, 86, 35, 57, 27)
    note(ax, 4, 52, "orange = LoRA target\n(query, value)\n  r = 8 or 16, α = 16", ORANGE, 14)
    note(ax, 104, 34, "purple = also\nadapted in the\n'+FFN' variant", PURPLE, 13)
    note(ax, 4, 30, "IA3: scales key + value\n(07b also the 3072-d\ninput of output.dense)", BLUE, 13)
    save(fig, "lora_where.png")


def qlora():
    fig, ax = canvas("QLoRA = 4-bit frozen base model + LoRA adapters (not quantised)")
    matrix(ax, 4, 38, 30, 24, BLUE, "W0 stored in\n4-bit NF4\n(frozen)", "≈ 4× smaller than fp16", hatch="..")
    arrow(ax, 34.8, 50, 46, 50, BLUE, "dequantise\non the fly", 13, tdy=1.5)
    matrix(ax, 47, 40, 20, 20, BLUE, "W0 in fp16\n(temporary,\nfor this matmul)", None, fs=13)
    matrix(ax, 72, 54, 22, 8, ORANGE, "LoRA A, B (full precision)", "trained, never quantised", fs=13)
    ax.add_patch(plt.Circle((104, 50), 3.2, fc="white", ec="#333", lw=2))
    ax.text(104, 50, "+", ha="center", va="center", fontsize=22)
    arrow(ax, 67.5, 50, 100.6, 50)
    arrow(ax, 94.5, 58, 101.5, 52.5, ORANGE)
    arrow(ax, 107.4, 50, 118, 50)
    ax.text(119, 50, "h", fontsize=20, va="center", weight="bold")
    box(ax, 4, 4, 56, 24, "Three memory tricks:\n1. NF4 4-bit storage of the frozen weights\n2. Double quantisation: the per-block scale\n    constants are quantised too\n3. Paged optimizer: optimizer state can spill\n    to CPU RAM if the GPU runs out", BLUE, 14)
    box(ax, 64, 4, 57, 24, "Compute is NOT done in 4 bit: weights are\ndequantised to fp16 (compute dtype; T4 has no bf16).\nGradients flow through the frozen W0 into A and B only.\nOurs: r = 16, α = 16 · peak 943 MiB vs 4,997 MiB\nfor full FT · macro-F1 0.363", GREEN, 14)
    save(fig, "qlora.png")


def nf4():
    fig, ax = plt.subplots(1, 2, figsize=(12.4, 6.2), dpi=100)
    from statistics import NormalDist
    xs = np.linspace(-1, 1, 400)
    q = np.array([NormalDist().inv_cdf(p) for p in np.linspace(0.02, 0.98, 16)])
    q = q / np.abs(q).max()
    for a, levels, title, col in [(ax[0], np.linspace(-1, 1, 16), "Evenly spaced 4-bit levels (INT4-like)", RED),
                                  (ax[1], q, "NF4: levels follow the normal distribution", GREEN)]:
        dens = np.exp(-xs ** 2 / (2 * 0.3 ** 2))
        a.fill_between(xs, dens, color="#dce8f7")
        a.plot(xs, dens, color=BLUE, lw=2, label="how weights are distributed")
        a.vlines(levels, 0, 1.08, color=col, lw=1.8)
        a.set_title(title, fontsize=15, weight="bold")
        a.set_yticks([])
        a.set_xlabel("weight value (scaled to [−1, 1] per block)")
        a.spines[["top", "right", "left"]].set_visible(False)
    ax[0].legend(loc="upper left", fontsize=11, frameon=False)
    fig.suptitle("4 bits = 16 possible values. NF4 puts more of them where most weights are (near 0) → less rounding error",
                 fontsize=15)
    fig.tight_layout()
    save(fig, "nf4.png")


def ia3():
    fig, ax = canvas("IA3: learn one scaling number per channel (no matrices at all)")
    for i, (name, vec) in enumerate([("keys  K", "l_k"), ("values  V", "l_v"), ("FFN 3072-d (07b only)", "l_ff")]):
        y = 58 - i * 17
        matrix(ax, 6, y, 30, 10, GREY, name, None, fs=15)
        ax.text(41, y + 5, r"$\odot$", fontsize=30, ha="center", va="center")
        for j in range(10):
            ax.add_patch(Rectangle((46 + j * 2.2, y + 2), 2, 6, fc=LIGHT[PURPLE], ec=PURPLE, lw=1.2))
        ax.text(57, y - 1.2, f"{vec}  (learned vector, starts at 1)", ha="center", va="top", fontsize=12, color=PURPLE)
        arrow(ax, 69, y + 5, 79, y + 5)
        matrix(ax, 80, y, 30, 10, BLUE, f"rescaled {name.split()[0]}", None, fs=14)
    box(ax, 4, 2, 117, 16, "$\\odot$ = element-wise multiply: channel i is multiplied by l[i]. It can only amplify or dampen what the model\n"
        "already computes, so it has far fewer parameters than LoRA (ours: 611,331 incl. the classifier head for XLM-R).\n"
        "Fewer knobs → cheaper, but less able to adapt: on XLM-R, IA3 scored lowest of the four methods (macro-F1 ≈ 0.24).", GREY, 14)
    save(fig, "ia3.png")


def tokenizer_fertility():
    fig, ax = canvas("Tokenizer fertility = tokens per word (lower = word kept more whole)")
    sent = "yeh film bohat achi thi"
    ax.text(62, 70, f"Roman Urdu sentence: \"{sent}\"   (5 words)", ha="center", fontsize=17)
    rows = [("Tokenizer A", ["▁yeh", "▁film", "▁bohat", "▁achi", "▁thi"], GREEN),
            ("Tokenizer B", ["▁ye", "h", "▁film", "▁bo", "hat", "▁ach", "i", "▁thi"], ORANGE)]
    for r, (name, toks, col) in enumerate(rows):
        y = 50 - r * 20
        ax.text(4, y + 4, name, fontsize=16, weight="bold", va="center", color=col)
        x = 24
        for t in toks:
            w = 3 + 1.6 * len(t)
            ax.add_patch(FancyBboxPatch((x, y), w, 8, boxstyle="round,pad=0.3", fc=LIGHT[col], ec=col, lw=1.8))
            ax.text(x + w / 2, y + 4, t, ha="center", va="center", fontsize=14)
            x += w + 1.6
        ax.text(x + 3, y + 4, f"{len(toks)} tokens / 5 words = {len(toks) / 5:.1f}", fontsize=15, va="center")
    box(ax, 4, 2, 117, 16, "Illustration only (made-up split). Higher fertility → words are chopped into more pieces, sequences get longer,\n"
        "and meaning is spread over fragments. We also report UNK rate (unknown tokens) and how many texts get truncated\n"
        "at max_length. Our measured values are in the fertility figure of the report.", GREY, 14)
    save(fig, "tokenizer_fertility.png")


if __name__ == "__main__":
    for fn in (ddpm_chain, x0hat_clipping, vit_tokens, swin_stages, linear_probe, finetune_vs_peft, lora,
               lora_where, qlora, nf4, ia3, tokenizer_fertility):
        fn()
        print("ok", fn.__name__)
