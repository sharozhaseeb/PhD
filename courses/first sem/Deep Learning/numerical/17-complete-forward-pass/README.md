# 17. A complete network forward pass

Every weighted sum, sigmoid and loss for the shared five-neuron network, followed by a full fresh-input practice.

[Open the PDF](lesson.pdf)

Lecture reference: Backpropagation_Derivation.pdf pages 1-2; numerical-practice.md N3.4 and N3.5 chosen parameters and examples.

## Illustrated walkthrough

### 1. Forward means calculate the prediction

![Forward means calculate the prediction](pages/page-01.png)

### 2. Start from the original study parameters

![Start from the original study parameters](pages/page-02.png)

### 3. Layer 1, neuron 1

![Layer 1, neuron 1](pages/page-03.png)

### 4. Layer 1, neuron 2

![Layer 1, neuron 2](pages/page-04.png)

### 5. Layer 2, neuron 1

![Layer 2, neuron 1](pages/page-05.png)

### 6. Layer 2, neuron 2

![Layer 2, neuron 2](pages/page-06.png)

### 7. Layer 3: the output neuron

![Layer 3: the output neuron](pages/page-07.png)

### 8. Use the probability in binary cross-entropy

![Use the probability in binary cross-entropy](pages/page-08.png)

### 9. Keep a forward cache for backpropagation

![Keep a forward cache for backpropagation](pages/page-09.png)

### 10. Your turn: a different input and target

![Your turn: a different input and target](pages/page-10.png)

### 11. Practice: layer 1, neuron 1

![Practice: layer 1, neuron 1](pages/page-11.png)

### 12. Practice: layer 1, neuron 2

![Practice: layer 1, neuron 2](pages/page-12.png)

### 13. Practice: layer 2, neuron 1

![Practice: layer 2, neuron 1](pages/page-13.png)

### 14. Practice: layer 2, neuron 2

![Practice: layer 2, neuron 2](pages/page-14.png)

### 15. Practice: layer 3: the output neuron

![Practice: layer 3: the output neuron](pages/page-15.png)

### 16. Practice answer: loss for target zero

![Practice answer: loss for target zero](pages/page-16.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
