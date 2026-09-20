# 18. Output-layer backpropagation

Derive sigmoid/BCE delta, calculate every output gradient, and verify sensitivity with a target-flip practice.

[Open the PDF](lesson.pdf)

Lecture reference: Backpropagation_Derivation.pdf pages 2-3, sections 4-5.2; numerical-practice.md N3.4 and N3.6.

## Illustrated walkthrough

### 1. Start from the saved forward pass

![Start from the saved forward pass](pages/page-01.png)

### 2. Delta measures sensitivity to preactivation

![Delta measures sensitivity to preactivation](pages/page-02.png)

### 3. Differentiate binary cross-entropy

![Differentiate binary cross-entropy](pages/page-03.png)

### 4. Cancel the sigmoid derivative once

![Cancel the sigmoid derivative once](pages/page-04.png)

### 5. Check both factors numerically

![Check both factors numerically](pages/page-05.png)

### 6. First output weight: use its source activation

![First output weight: use its source activation](pages/page-06.png)

### 7. Second output weight: keep its own source

![Second output weight: keep its own source](pages/page-07.png)

### 8. Output bias: the source is constant one

![Output bias: the source is constant one](pages/page-08.png)

### 9. What does a negative gradient predict?

![What does a negative gradient predict?](pages/page-09.png)

### 10. Your turn: flip only the known target

![Your turn: flip only the known target](pages/page-10.png)

### 11. Practice answer: prediction stays the same

![Practice answer: prediction stays the same](pages/page-11.png)

### 12. Practice answer: all three output gradients

![Practice answer: all three output gradients](pages/page-12.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
