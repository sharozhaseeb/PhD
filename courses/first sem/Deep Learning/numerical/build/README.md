# Rebuilding the numerical lessons

Each lesson stores its authored content in `lesson.json`. Run:

```powershell
python numerical/build/render_lesson.py numerical/01-single-feature-linear-regression/lesson.json
```

Run from the Deep Learning directory. The renderer creates `lesson.pdf`, image pages and the Obsidian `README.md` beside the specification. Dependencies: Python, ReportLab, matplotlib, Pillow and Poppler. The default Poppler path uses the bundled Codex runtime; adjust it for another machine.

Rendering is not approval: every lesson must have a plan discussion, independent mathematical checks and a TA visual review. Approval records live in `numerical/reviews`.

Specifications use explicit pages rather than automatic dense pagination. Each page has a title, subtitle, and blocks of explanatory prose or typeset equations. Text and equation widths, and page content heights, are checked before a PDF is accepted.
