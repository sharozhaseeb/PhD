# 19. Hidden-layer backpropagation

Calculate every hidden delta and all twelve hidden gradients, including every branching path and a full target-flip practice.

[Open the PDF](lesson.pdf)

Lecture reference: Backpropagation_Derivation.pdf page 3, sections5.3-6; numerical-practice.md N3.4 and N3.6.

## Illustrated walkthrough

### 1. Continue backward from the output delta

![Continue backward from the output delta](pages/page-01.png)

### 2. Sum downstream paths, then apply the local slope

![Sum downstream paths, then apply the local slope](pages/page-02.png)

### 3. Hidden layer 2, neuron 1: delta

![Hidden layer 2, neuron 1: delta](pages/page-03.png)

### 4. Hidden layer 2, neuron 2: delta

![Hidden layer 2, neuron 2: delta](pages/page-04.png)

### 5. Layer 2, neuron 1: three gradients

![Layer 2, neuron 1: three gradients](pages/page-05.png)

### 6. Layer 2, neuron 2: three gradients

![Layer 2, neuron 2: three gradients](pages/page-06.png)

### 7. Hidden layer 1, neuron 1: delta

![Hidden layer 1, neuron 1: delta](pages/page-07.png)

### 8. Hidden layer 1, neuron 2: delta

![Hidden layer 1, neuron 2: delta](pages/page-08.png)

### 9. Layer 1, neuron 1: three gradients

![Layer 1, neuron 1: three gradients](pages/page-09.png)

### 10. Layer 1, neuron 2: three gradients

![Layer 1, neuron 2: three gradients](pages/page-10.png)

### 11. Why the first hidden neuron needs both paths

![Why the first hidden neuron needs both paths](pages/page-11.png)

### 12. Checkpoint: every hidden parameter is covered

![Checkpoint: every hidden parameter is covered](pages/page-12.png)

### 13. Your turn: propagate the target-flip delta

![Your turn: propagate the target-flip delta](pages/page-13.png)

### 14. Practice: Hidden layer 2, neuron 1: delta

![Practice: Hidden layer 2, neuron 1: delta](pages/page-14.png)

### 15. Practice: Hidden layer 2, neuron 2: delta

![Practice: Hidden layer 2, neuron 2: delta](pages/page-15.png)

### 16. Practice: Layer 2, neuron 1: three gradients

![Practice: Layer 2, neuron 1: three gradients](pages/page-16.png)

### 17. Practice: Layer 2, neuron 2: three gradients

![Practice: Layer 2, neuron 2: three gradients](pages/page-17.png)

### 18. Practice: Hidden layer 1, neuron 1: delta

![Practice: Hidden layer 1, neuron 1: delta](pages/page-18.png)

### 19. Practice: Hidden layer 1, neuron 2: delta

![Practice: Hidden layer 1, neuron 2: delta](pages/page-19.png)

### 20. Practice: Layer 1, neuron 1: three gradients

![Practice: Layer 1, neuron 1: three gradients](pages/page-20.png)

### 21. Practice: Layer 1, neuron 2: three gradients

![Practice: Layer 1, neuron 2: three gradients](pages/page-21.png)

### 22. Practice check: what changed and what did not?

![Practice check: what changed and what did not?](pages/page-22.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
