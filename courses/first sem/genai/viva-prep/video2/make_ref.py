import json, sys, fitz
from pathlib import Path
R = Path(__file__).parent / "ref"
G = Path(r"C:/Users/pc/study/PhD/courses/first sem/genai")
for k in ("A2", "A3"):
    d = fitz.open(R / f"{k}_handout.pdf")
    with open(R / f"{k}_handout_pages.txt", "w", encoding="utf-8") as f:
        for i, p in enumerate(d):
            f.write(f"\n===== PAGE {i+1} =====\n" + p.get_text())
nb = json.load(open(G / "assignment-2/colab_run/26L-9005_A2_executed.ipynb", encoding="utf-8"))
lines = []
for i, c in enumerate(nb["cells"]):
    src = "".join(c["source"])
    lines.append(f"# ===== CELL {i} ({c['cell_type']}) =====")
    lines += src.splitlines()
(R / "A2_notebook_cells.txt").write_text("\n".join(lines), encoding="utf-8")

# ---- executed-notebook OUTPUTS (noise lines filtered), same cell markers as the code dumps
import re
NOISE = re.compile(r"absl::InitializeLog|cpu_feature_guard|To enable the following instructions|cudart_stub|FutureWarning|torch\._check|_check_is_size|Some weights of|You should probably TRAIN|IPython\.core\.display|^\s*warnings\.warn|UserWarning|TensorFlow binary")
for k, path in (("A2", G / "assignment-2/colab_run/26L-9005_A2_executed.ipynb"),
                ("A3", G / "assignment-3/output/Group3_Assignment3/Group3_Colab_Executed.ipynb")):
    nb = json.load(open(path, encoding="utf-8"))
    out = []
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code" or not c.get("outputs"):
            continue
        out.append(f"# ===== CELL {i} (output) =====")
        for o in c["outputs"]:
            if "text" in o:
                txt = "".join(o["text"])
            elif "data" in o:
                txt = "".join(o["data"].get("text/plain", "")) if "image/png" not in o["data"] else "[figure shown in notebook]"
            elif o.get("output_type") == "error":
                txt = f"{o.get('ename')}: {o.get('evalue')}"
            else:
                txt = ""
            out += [l for l in txt.replace("\r", "\n").splitlines() if l.strip() and not NOISE.search(l)]
    (R / f"{k}_notebook_outputs.txt").write_text("\n".join(out), encoding="utf-8")
    print(k, len(out), "output lines")
