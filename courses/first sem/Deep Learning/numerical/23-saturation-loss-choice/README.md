# 23. Sigmoid saturation and loss choice

Compare half-squared error and BCE on the same wrong prediction, derive every gradient, and work both parameter updates with a fresh practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture4 PDF pages8-26: saturation/squared divergence, unhalved formula page12; Backpropagation_Derivation.pdf page2: sigmoid+BCE; numerical-practice.md N4.1. Half-square study convention explicitly labeled.

## Illustrated walkthrough

### 1. The same wrong prediction, two loss functions

![The same wrong prediction, two loss functions](pages/page-01.png)

### 2. State the loss scaling before differentiating

![State the loss scaling before differentiating](pages/page-02.png)

### 3. Half-squared error keeps the small sigmoid slope

![Half-squared error keeps the small sigmoid slope](pages/page-03.png)

### 4. BCE cancels the sigmoid factor

![BCE cancels the sigmoid factor](pages/page-04.png)

### 5. Translate each output derivative into parameters

![Translate each output derivative into parameters](pages/page-05.png)

### 6. one step with half-squared error

![one step with half-squared error](pages/page-06.png)

### 7. one step with BCE

![one step with BCE](pages/page-07.png)

### 8. Why the logit change contains x-squared

![Why the logit change contains x-squared](pages/page-08.png)

### 9. Where sigmoid becomes insensitive

![Where sigmoid becomes insensitive](pages/page-09.png)

### 10. Your turn: a wrong target-zero prediction

![Your turn: a wrong target-zero prediction](pages/page-10.png)

### 11. Practice: losses and full chain-rule arithmetic

![Practice: losses and full chain-rule arithmetic](pages/page-11.png)

### 12. Practice: one step with half-squared error

![Practice: one step with half-squared error](pages/page-12.png)

### 13. Practice: one step with BCE

![Practice: one step with BCE](pages/page-13.png)

### 14. Practice checks and the scope of the conclusion

![Practice checks and the scope of the conclusion](pages/page-14.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
