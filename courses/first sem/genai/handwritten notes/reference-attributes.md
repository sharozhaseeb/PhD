# Attributes extracted from the Deep Learning handwritten references

Reviewed all three PNGs in `../../Deep Learning/handwritten notes/`. The references are three presentations of the same backpropagation/weight-update example, rather than three unrelated lecture summaries. Their main strength is teaching a reproducible solution method while retaining the reason for each step.

## Pedagogical pattern to reproduce

1. **Name one concrete question.** The title states the concept and the task, such as “Chain Rule — updating w5.” Start with what the learner is trying to find and why it matters.
2. **Provide the givens before calculation.** Numerical values, targets, relevant intermediate outputs, and parameter values appear next to a small diagram.
3. **Show the dependency or architecture.** Arrows identify the path through which the objective depends on the variable. A diagram clarifies the formula rather than acting as decoration.
4. **State the general rule before inserting numbers.** The chain rule or update equation is visible and boxed. Symbol definitions appear nearby.
5. **Break the procedure into numbered steps.** Each local derivative gets its own short explanation; arithmetic follows directly beneath it.
6. **Show a complete worked example.** Formula → substitution → intermediate values → boxed result. The learner can reconstruct the method without guessing omitted operations.
7. **Interpret the result.** Explain what the value means and the direction of the update. Include a short takeaway explaining the general idea, not only the answer.
8. **Compare related methods using the same givens.** Gradient descent and momentum reuse the starting example, making differences easier to understand.
9. **Keep background selective.** Include theory needed to define, explain, compare, or solve. Avoid lecture-transcript prose and lists of applications that overwhelm the mathematical core.

## Visual attributes

- Light warm-white ruled notebook paper, faint grey horizontal lines, a thin red left margin, and generous clean edges.
- Readable blue handwritten body text and equations; handwriting is tidy with mild natural variation.
- A prominent underlined blue title, with a pale pink highlighter strip.
- Short numbered subsection headings in dark pink/red, usually with pink highlighting or underlining.
- Thin green boxes around important formulas and final numerical answers; occasional blue boxes for the end-of-page summary.
- Broad single-column derivations, or two balanced columns divided by a thin blue line when content benefits from side-by-side comparison.
- Small hand-drawn architecture diagrams with labelled circles and arrows. Diagram labels must remain clear at normal reading size.
- Equations are aligned vertically; substituted expressions stay adjacent to their parent formula. Fractions, subscripts, and superscripts are visibly distinct.
- The page is dense enough to be useful but has whitespace between numbered steps. Avoid copying camera perspective, page warping, shadows, or peripheral clutter: those add no instructional value.

## Page-design rules for GenAI

- Give each page one main exam task or a tightly related theory-and-numerical pair. Do not force an entire long lecture onto one image.
- Begin with a short concept/goal, then a diagram or comparison when useful, core formulas with defined symbols, one complete worked numerical, and 2–4 concise takeaways or exam traps.
- Theory pages may use an illustrative example instead of artificial arithmetic. Numerical pages must include givens, assumptions, the requested quantity, all essential calculation steps, and a final interpretation.
- Aim for 4–6 meaningful blocks per page. If an example needs cramped writing, split the page; readable handwriting takes precedence over a page-count target.
- Reuse a numerical setting across neighbouring pages only when it makes comparison easier; each page must still provide sufficient givens to stand alone.
- Include lecture/page identifiers unobtrusively. Distinguish an original study example from a numerical printed in the lecture.
- Use full lecture PDFs as the authority for scope. The existing support guide and numerical-practice file can supply explanations and examples, but must be reconciled with the slides.
- Cover all four available decks: Introduction; AE/VAE; GANs Part 1; GANs Part 2. Mention later model families only at the introductory depth supplied by Lecture 1; do not create absent lectures.

## Mathematical and clarity safeguards

- Freeze approved page text and equations before image generation. Treat generation as rendering, never as a source of new mathematics.
- Define natural logarithms unless another base is intended; specify sum versus mean, per sample versus batch, and any loss weighting.
- Keep variance `sigma^2`, standard deviation `sigma`, and `logvar = ln(sigma^2)` distinct. State whether an encoder outputs variance or log variance.
- For VAE pages distinguish reconstruction loss, KL divergence, negative ELBO, and optional beta weighting. Label simplifications and toy decoder assumptions.
- For GAN pages distinguish discriminator maximization from loss minimization, saturating from non-saturating generator loss, and whether discriminator parameters are held fixed during a generator step.
- For Bayes, show the normalizing denominator. For sampling tables, verify nonnegative probabilities and total one. For IS/FID, define the averaging and distribution assumptions.
- Use adequate intermediate precision and round only the displayed final result. Do not copy the reference momentum example's intermediate rounding as a precision policy.
- Select one RMSProp epsilon convention consistently if that prerequisite ever appears: the references show epsilon under the root in one formula but outside it in the worked substitution. This inconsistency should not be reproduced.
- Check every generated digit, sign, subscript, bracket, arrow, and formula. A visually plausible page can still contain an incorrect equation or missing definition.

## Independent review gates

1. **Plan clearance:** each page has a title, source slide range, precise learning goals, complete theory statements, equations with definitions, verified numerical values and interpretation, proposed visual layout, and an overflow alternative. Across pages, all substantive available lecture topics are accounted for.
2. **Phase 1 review:** inspect every generated PNG for the first two lectures against its approved page specification. Check content, arithmetic, notation, readability, omissions, visual consistency, and whether it can be studied independently. Regenerate or correct failures before phase 2.
3. **Phase 2 review:** perform the same checks for both GAN decks, and confirm the final file/page inventory matches the cleared plan.

The references establish a strong instructional format, not a guarantee of mathematical accuracy. Preserve their explanatory structure and visual hierarchy while independently verifying the new content.
