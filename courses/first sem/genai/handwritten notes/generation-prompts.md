# Image generation prompt set

Mode: built-in imagegen. The Deep Learning PNGs are style references, not edit targets.

Shared prompt:

```text
Use case: scientific-educational.
Create ONE high-resolution handwritten study-note PNG page, portrait, completely visible with clean uncut margins, approximately A4 proportions. This is a new Gen AI exam revision page.
Match the supplied Deep Learning reference images ONLY for notebook style: warm white faintly ruled paper, subtle red left margin, tidy natural blue-ink handwriting, blue title over pale pink highlighter, dark burgundy numbered section headings, thin green boxes for the central formula and final numeric answers. Use a balanced two-column layout where appropriate; larger clear handwriting and generous spacing. Minimal helpful hand-drawn arrow diagrams. No camera skew, hands, shadows, decoration, watermarks, logos or invented equations.
Accuracy is critical. Render ALL approved content below, faithfully, in order, preserving every minus sign, decimal, superscript/subscript, fraction, direction of KL, log, assumption and numerical value. Proper mathematical handwritten notation rather than raw typesetting codes. Do not add claims or numbers. Never cut or overlap text. Use the available page efficiently with legible lines. Keep related equation, substitution and result together. Heading and footer need not repeat source filenames.
```

Each call appends the matching page title, exact approved content from `page-manifest.json`, and a footer with page ID and lecture source page positions. Any regenerated version uses the same full page content plus a targeted correction. Per-page approved text is also readable in `plan.md`.

Output files are copied into this folder from the imagegen save location. Reviewer gates are recorded in `review-log.md`.

## Targeted review corrections

- L2-03-v2: edit only to add “Draw ε ~ N(0,I) (standard normal noise); ⊙ = elementwise multiply.” Preserve all original page content and style.
- L2-06-v2: edit only the ambiguous A-example KL label to clearly read “K_A = 2.125”; retain R_A=0.05125 and L_A=2.17625.
- L4-02-v2: edit only the diagram to show a clear sketch arrow from Stage I output into Stage II; retain the text-condition input label and the rest of the page unchanged.

Final selected versions were re-inspected by root and the independent reviewer.
