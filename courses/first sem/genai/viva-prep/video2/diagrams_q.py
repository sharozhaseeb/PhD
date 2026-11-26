"""Extra concept diagrams for the viva-questions videos (saved to diagrams/)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

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
    ax.text(62, 82, title, ha="center", va="center", fontsize=21, weight="bold", color="#222")
    return fig, ax


def box(ax, x, y, w, h, text, color=BLUE, fs=13, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.0",
                                fc=LIGHT[color], ec=color, lw=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight, color="#222")


def arrow(ax, x0, y0, x1, y1, color="#444", lw=2, style="-|>"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=16, color=color, lw=lw))


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------ Swin + FPN (vs ViT single scale)
fig, ax = canvas("Why Swin plugs into an FPN for detection, and plain ViT does not")
ax.text(4, 75, "Image 224 × 224", fontsize=13, weight="bold")
# Swin stages (bottom = high resolution)
stages = [("Stage 1\n56×56×96\nstride 4", 8), ("Stage 2\n28×28×192\nstride 8", 24),
          ("Stage 3\n14×14×384\nstride 16", 40), ("Stage 4\n7×7×768\nstride 32", 56)]
ws = [22, 18, 14, 10]
for (t, y), w in zip(stages, ws):
    box(ax, 4 + (22 - w) / 2, y, w, 11, t, BLUE, fs=11)
for k in range(3):
    arrow(ax, 15, stages[k][1] + 11, 15, stages[k + 1][1], BLUE)
ax.text(15, 69.5, "Swin-T backbone\n(features_only=True)", ha="center", fontsize=12, color=BLUE, weight="bold")
ax.text(28.5, 31, "Patch Merging\nhalves the grid", fontsize=10, color=BLUE, rotation=90, va="center")
# FPN
names = ["P2", "P3", "P4", "P5"]
for k, (_, y) in enumerate(stages):
    box(ax, 50, y + 1, 12, 9, names[k], GREEN, fs=14, weight="bold")
    arrow(ax, 27, y + 5.5, 50, y + 5.5, ORANGE)
    ax.text(38.5, y + 7, "1×1 conv\n(lateral)", ha="center", fontsize=9.5, color=ORANGE)
for k in range(3, 0, -1):
    arrow(ax, 59, stages[k][1] + 1, 59, stages[k - 1][1] + 10, GREEN)
    ax.text(60.5, stages[k][1] - 2.5, "×2 upsample\n+ add", fontsize=9.5, color=GREEN)
ax.text(56, 69.5, "FPN\n(top-down + lateral)", ha="center", fontsize=12, color=GREEN, weight="bold")
for k, (_, y) in enumerate(stages):
    arrow(ax, 62, y + 5.5, 70, y + 5.5)
box(ax, 70, 10, 14, 54, "Detection heads\n(boxes + classes)\n\nsmall objects\n→ P2\n\nlarge objects\n→ P5", PURPLE, fs=11)
# ViT column
box(ax, 92, 52, 28, 12, "ViT-B/16\n14×14 tokens × 768\nat EVERY layer (stride 16)", RED, fs=11)
box(ax, 92, 32, 28, 14, "Only one scale → nothing\nfor an FPN to combine.\nNeeds extra adapters\n(e.g. ViTDet's simple pyramid)", RED, fs=10.5)
arrow(ax, 106, 52, 106, 46, RED)
box(ax, 92, 6, 28, 20, "Our A2: classification +\nfeature probing only.\nfeatures_only=True gives\nthe 4 maps an FPN\nwould receive.", GREY, fs=10.5)
save(fig, "swin_fpn.png")

# ------------------------------------------------------------ why sampling depends on t
fig, ax = canvas("Sampling: why every reverse step needs its timestep t")
xs = [6, 34, 62, 90]
labels = ["$x_T \\sim N(0, I)$\npure noise\nt = 999", "$x_{500}$\nt = 500", "$x_{50}$\nt = 50", "$x_0$\nclean image"]
cols = [GREY, BLUE, BLUE, GREEN]
for x, l, c in zip(xs, labels, cols):
    box(ax, x, 56, 22, 14, l, c, fs=13)
for k in range(3):
    arrow(ax, xs[k] + 22, 63, xs[k + 1], 63, "#444", lw=2.4)
ax.text(62, 52, "one small denoising step at a time:  t = 999 → 998 → … → 0", ha="center", fontsize=13)
box(ax, 6, 20, 52, 24, "", ORANGE)
ax.text(32, 40, "Inside one step at time t", ha="center", fontsize=14, weight="bold")
ax.text(32, 29, r"1. U-Net gets ($x_t$, $t$): time embedding" "\n" r"    tells it HOW noisy $x_t$ is" "\n"
                r"2. predicts noise $\hat{\epsilon}$ → $\hat{x}_0$, clipped to [−1, 1]" "\n"
                r"3. $x_{t-1}$ = mean($x_t$, $\hat{\epsilon}$; $\alpha_t, \bar{\alpha}_t, \beta_t$) + $\sigma_t z$",
        ha="center", fontsize=12, va="center")
box(ax, 64, 20, 54, 24, "", PURPLE)
ax.text(91, 40, "t is used twice", ha="center", fontsize=14, weight="bold")
ax.text(91, 29, "• as INPUT to the network\n  (noise level differs per step)\n"
                r"• to LOOK UP $\alpha_t, \bar{\alpha}_t, \beta_t, \sigma_t$" "\n  from the schedule (linear / cosine)",
        ha="center", fontsize=12, va="center")
box(ax, 6, 3, 112, 12, "Wrong t → wrong noise estimate and wrong coefficients → blurry or noisy samples.\n"
                      "Skipping steps needs a different sampler (e.g. DDIM); plain DDPM must visit every t.", RED, fs=12)
save(fig, "sampling_t.png")
print("ok")
