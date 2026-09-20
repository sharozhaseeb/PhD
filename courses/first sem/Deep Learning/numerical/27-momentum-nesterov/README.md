# 27. Momentum and Nesterov, step by step

Track signed displacement and the exact gradient location through two updates, compare plain GD, and solve a fresh changed-curvature practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture4 PDF pages75-93, especially page90 signed Delta-W Nesterov equation. v denotes signed parameter displacement. numerical-practice.md N4.6.

## Illustrated walkthrough

### 1. Momentum carries a signed displacement forward

![Momentum carries a signed displacement forward](pages/page-01.png)

### 2. Nesterov changes where the gradient is evaluated

![Nesterov changes where the gradient is evaluated](pages/page-02.png)

### 3. Plain gradient descent gives a useful baseline

![Plain gradient descent gives a useful baseline](pages/page-03.png)

### 4. Momentum, update 1

![Momentum, update 1](pages/page-04.png)

### 5. Momentum, update 2

![Momentum, update 2](pages/page-05.png)

### 6. Nesterov, update 1

![Nesterov, update 1](pages/page-06.png)

### 7. Nesterov, update 2

![Nesterov, update 2](pages/page-07.png)

### 8. Trace Nesterov second-step dependencies

![Trace Nesterov second-step dependencies](pages/page-08.png)

### 9. Compare all second-step states

![Compare all second-step states](pages/page-09.png)

### 10. Your turn: new curvature and momentum coefficient

![Your turn: new curvature and momentum coefficient](pages/page-10.png)

### 11. Practice: derivative and gradient-descent baseline

![Practice: derivative and gradient-descent baseline](pages/page-11.png)

### 12. Practice: Momentum, update 1

![Practice: Momentum, update 1](pages/page-12.png)

### 13. Practice: Momentum, update 2

![Practice: Momentum, update 2](pages/page-13.png)

### 14. Practice: Nesterov, update 1

![Practice: Nesterov, update 1](pages/page-14.png)

### 15. Practice: Nesterov, update 2

![Practice: Nesterov, update 2](pages/page-15.png)

### 16. Practice checkpoint and common mistakes

![Practice checkpoint and common mistakes](pages/page-16.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
