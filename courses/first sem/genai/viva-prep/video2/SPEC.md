# Slide script format for the slower walkthrough videos

The viewer is the student, about to have an individual viva. They do **not** fully understand the underlying concepts, so:
- Explain each idea in plain words *before* the jargon. Use small analogies, and say what each symbol means each time it appears.
- Use a calm, friendly, conversational teacher voice. Say "you" and "we", use short sentences, and pause naturally with full stops. Don't race.
- Narration is spoken by a text-to-speech voice, so write it as speech:
  - spell symbols as words ("alpha bar t", "beta", "x zero", "epsilon")
  - no markdown and no parentheses-heavy text
  - write numbers as they should be read ("five times ten to the minus four", "0.419")
- Never mention AI tools, assistants or "Claude" anywhere.
- Be factually exact. Every number must come from the result files or reports listed in your brief. If you are unsure, leave it out.

## The flow for every handout requirement

Repeat this loop for each task the handout asks for:
1. **handout slide:** show the exact handout lines, highlighted, and say in plain words what is being asked and why the instructor asks it.
2. **concept slide** (optional, `kind="text"`): the idea in simple terms.
3. **code slide:** the actual code we wrote for it, explained line by line, plus the design decision and *why* we chose it over the alternatives.
4. **result slide:** the figure or numbers we got, how to read them, and what they mean.
5. Optionally, a **"viva check"** text slide: two or three likely questions on this task, each with a short spoken answer.

## File format

Write a Python file that defines `SLIDES = [ ... ]`, a list of dicts. Each dict has these keys:

```python
dict(
  section="Part A",               # short chapter name; consecutive slides share it
  title="A1 · What the handout asks",
  kind="handout",                 # one of: "handout", "code", "figure", "text"
  # kind="handout":
  page=2,                         # 1-based page of the handout PDF
  find=["Implement two noise schedules", "linear schedule"],
      # 1-4 SHORT phrases (3-10 words). Copy them EXACTLY from ONE line of the
      # page dump (ref/<A>_handout_pages.txt): same spelling and punctuation, and
      # never spanning a line break. They are highlighted, and the crop is centred on them.
  # kind="code":
  src="A2NB",                     # "A2NB" = ref/A2_notebook_cells.txt; "A3SRC" = A3 train_group3.py; "A3NB" = ref/A3_notebook_cells.txt
  start="def q_sample(",          # exact substring of the FIRST line to show (it must be unique in that file; if not, make it longer)
  n=14,                           # number of lines to show (max 22)
  # kind="figure":
  image="A2F/A1_alpha_bar.png",   # prefixes: A2F/ = A2 figures, A3F/ = A3 figures
  image2=None,                    # optional second image, shown below the first
  bullets=["...", "..."],         # 2-5 short on-screen points, each under 90 characters (handout/code/figure slides show them in a side panel)
  narration="...",                # what the voice says: 90-230 words, conversational, explained slowly
)
```

`kind="text"` slides show only the title and the bullets; use up to 6 bullets there.

Keep the on-screen bullets short. The narration carries the explanation.

## Additions (code-walkthrough revision)

**New sources for `kind="code"`:**
- `A3PRE` = A3 source/track3_preflight.py
- `A3COL` = source/collect_results.py
- `A3FIG` = source/make_figures.py
- `A3REC` = source/run_recovery.py

**New `kind="output"`:** shows the SAVED output of the executed Colab notebook, from the earlier run. Nothing is re-run.
- `src`: `"A3OUT"` (ref/A3_notebook_outputs.txt) or `"A2OUT"` (ref/A2_notebook_outputs.txt). Both files use the same "# ===== CELL k (output) =====" markers.
- `start`: an exact substring of the first output line to show. It must be unique in the file.
- `n`: up to 30 lines. Long lines wrap, and about 25 wrapped rows fit.

**Optional `hl=["substring", ...]` on code and output slides:** every shown line containing one of these substrings gets a yellow highlight. Use it to point at the exact line the narration is talking about. 1–4 substrings per slide.

**Code walkthrough style:**
- Narration walks through the highlighted lines one by one: "on line 115 we call f1 score with average equals macro, which means..."
- Say what each argument does and WHY we chose that value over the alternative.
- When a long function needs several screens, use several consecutive code slides with different `start` lines.
