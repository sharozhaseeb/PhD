# 35. Dropout: full masked forward and backward passes

Trace all seven parameter gradients and updates under a fixed mask, compare standard/inverted scaling and inference, enumerate masks, and solve the opposite-mask practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture 5 pages144-158; forward153, backward154, expectation approximation155, inference scaling156. numerical-practice.md N6.8 seven-parameter study network. Inverted dropout is a labeled comparison.

## Illustrated walkthrough

### 1. Drop hidden activations with a fixed binary mask

![Drop hidden activations with a fixed binary mask](pages/page-01.png)

### 2. Define all seven trainable parameters

![Define all seven trainable parameters](pages/page-02.png)

### 3. Follow the two hidden paths

![Follow the two hidden paths](pages/page-03.png)

### 4. Main pass: hidden activations

![Main pass: hidden activations](pages/page-04.png)

### 5. Main pass: mask, output and loss

![Main pass: mask, output and loss](pages/page-05.png)

### 6. Main pass: output gradients

![Main pass: output gradients](pages/page-06.png)

### 7. Main pass: hidden deltas

![Main pass: hidden deltas](pages/page-07.png)

### 8. Main pass: input weights and hidden biases

![Main pass: input weights and hidden biases](pages/page-08.png)

### 9. Main pass: update hidden parameters

![Main pass: update hidden parameters](pages/page-09.png)

### 10. Main pass: update output parameters

![Main pass: update output parameters](pages/page-10.png)

### 11. Main pass: check the updated pass

![Main pass: check the updated pass](pages/page-11.png)

### 12. Standard-dropout inference: reset original parameters

![Standard-dropout inference: reset original parameters](pages/page-12.png)

### 13. Inverted comparison: hidden activations

![Inverted comparison: hidden activations](pages/page-13.png)

### 14. Inverted comparison: mask, output and loss

![Inverted comparison: mask, output and loss](pages/page-14.png)

### 15. Inverted comparison: output gradients

![Inverted comparison: output gradients](pages/page-15.png)

### 16. Inverted comparison: hidden deltas

![Inverted comparison: hidden deltas](pages/page-16.png)

### 17. Inverted comparison: input weights and hidden biases

![Inverted comparison: input weights and hidden biases](pages/page-17.png)

### 18. Inverted-dropout inference: original parameters

![Inverted-dropout inference: original parameters](pages/page-18.png)

### 19. Enumerate all masks at the original state

![Enumerate all masks at the original state](pages/page-19.png)

### 20. Nonlinear output: expectation is only approximated

![Nonlinear output: expectation is only approximated](pages/page-20.png)

### 21. Your turn: keep the other hidden unit

![Your turn: keep the other hidden unit](pages/page-21.png)

### 22. Practice: hidden activations

![Practice: hidden activations](pages/page-22.png)

### 23. Practice: mask, output and loss

![Practice: mask, output and loss](pages/page-23.png)

### 24. Practice: output gradients

![Practice: output gradients](pages/page-24.png)

### 25. Practice: hidden deltas

![Practice: hidden deltas](pages/page-25.png)

### 26. Practice: input weights and hidden biases

![Practice: input weights and hidden biases](pages/page-26.png)

### 27. Practice: update hidden parameters

![Practice: update hidden parameters](pages/page-27.png)

### 28. Practice: update output parameters

![Practice: update output parameters](pages/page-28.png)

### 29. Practice: check the updated pass

![Practice: check the updated pass](pages/page-29.png)

### 30. Answer: mask count and probability

![Answer: mask count and probability](pages/page-30.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
