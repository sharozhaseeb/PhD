# 33. Adam moments and bias correction

Calculate raw moments, correction powers, denominator and parameter updates through a gradient sign change; solve a fresh complete two-step practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture 5 PDF pages119-124, equations121-122. Slide delta maps to beta1 and gamma to beta2. numerical-practice.md N6.6 supplied-gradient examples, with positive-epsilon convention comparison.

## Illustrated walkthrough

### 1. Adam remembers direction and squared magnitude

![Adam remembers direction and squared magnitude](pages/page-01.png)

### 2. Read the raw and corrected moment formulas

![Read the raw and corrected moment formulas](pages/page-02.png)

### 3. Use the course denominator convention

![Use the course denominator convention](pages/page-03.png)

### 4. update 1: raw moments

![update 1: raw moments](pages/page-04.png)

### 5. update 1: bias correction

![update 1: bias correction](pages/page-05.png)

### 6. update 1: denominator and parameter

![update 1: denominator and parameter](pages/page-06.png)

### 7. update 2: raw moments

![update 2: raw moments](pages/page-07.png)

### 8. update 2: bias correction

![update 2: bias correction](pages/page-08.png)

### 9. update 2: denominator and parameter

![update 2: denominator and parameter](pages/page-09.png)

### 10. The latest gradient changed sign, but m did not

![The latest gradient changed sign, but m did not](pages/page-10.png)

### 11. Why dividing by 1 minus beta to the t helps

![Why dividing by 1 minus beta to the t helps](pages/page-11.png)

### 12. Two common correction errors

![Two common correction errors](pages/page-12.png)

### 13. Positive epsilon: the placement is visible

![Positive epsilon: the placement is visible](pages/page-13.png)

### 14. Your turn: repeat a negative gradient

![Your turn: repeat a negative gradient](pages/page-14.png)

### 15. Practice: update 1: raw moments

![Practice: update 1: raw moments](pages/page-15.png)

### 16. Practice: update 1: bias correction

![Practice: update 1: bias correction](pages/page-16.png)

### 17. Practice: update 1: denominator and parameter

![Practice: update 1: denominator and parameter](pages/page-17.png)

### 18. Practice: update 2: raw moments

![Practice: update 2: raw moments](pages/page-18.png)

### 19. Practice: update 2: bias correction

![Practice: update 2: bias correction](pages/page-19.png)

### 20. Practice: update 2: denominator and parameter

![Practice: update 2: denominator and parameter](pages/page-20.png)

### 21. Practice checkpoint: magnitude is not variability

![Practice checkpoint: magnitude is not variability](pages/page-21.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
