# 07. Computation graphs and the chain rule

Lecture graph forward and backward, then a branching-path extension.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture 2 - Logistic Regression + Neural Network.pdf, page 27; branching example is an original extension.

## Illustrated walkthrough

### 1. Break one expression into small steps

![Break one expression into small steps](pages/page-01.png)

### 2. Forward pass: save every node value

![Forward pass: save every node value](pages/page-02.png)

### 3. Local derivatives: inspect one operation

![Local derivatives: inspect one operation](pages/page-03.png)

### 4. Backward pass: multiply along each path

![Backward pass: multiply along each path](pages/page-04.png)

### 5. A shared input can affect two paths

![A shared input can affect two paths](pages/page-05.png)

### 6. At a branch, add the path contributions

![At a branch, add the path contributions](pages/page-06.png)

### 7. Your turn: include a negative input

![Your turn: include a negative input](pages/page-07.png)

### 8. Practice answer: follow values and paths

![Practice answer: follow values and paths](pages/page-08.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
