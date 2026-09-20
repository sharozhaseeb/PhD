# 24. Newton method and curvature correction

Solve a full Newton correction, compare gradient descent from the same point, and work a fresh practice with saddle/singular counterexamples.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture4 PDF pages33-36: scalar curvature; pages47-52: normalized multivariate update and Hessian issues, eta included on page50. numerical-practice.md N4.3.

## Illustrated walkthrough

### 1. Newton uses slope and curvature together

![Newton uses slope and curvature together](pages/page-01.png)

### 2. Map the lecture formula to a linear system

![Map the lecture formula to a linear system](pages/page-02.png)

### 3. Compute the mixed-quadratic ingredients

![Compute the mixed-quadratic ingredients](pages/page-03.png)

### 4. Solve for the Newton correction by elimination

![Solve for the Newton correction by elimination](pages/page-04.png)

### 5. Optional check: the two-by-two inverse

![Optional check: the two-by-two inverse](pages/page-05.png)

### 6. Compare gradient descent from the same start

![Compare gradient descent from the same start](pages/page-06.png)

### 7. Two alternative arrows from one starting point

![Two alternative arrows from one starting point](pages/page-07.png)

### 8. Why the exact quadratic finishes in one full step

![Why the exact quadratic finishes in one full step](pages/page-08.png)

### 9. An invertible Hessian can lead to a saddle

![An invertible Hessian can lead to a saddle](pages/page-09.png)

### 10. A singular Hessian makes the raw formula undefined

![A singular Hessian makes the raw formula undefined](pages/page-10.png)

### 11. Your turn: a fresh mixed quadratic

![Your turn: a fresh mixed quadratic](pages/page-11.png)

### 12. Practice: ingredients and elimination

![Practice: ingredients and elimination](pages/page-12.png)

### 13. Practice: both updates and both losses

![Practice: both updates and both losses](pages/page-13.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
