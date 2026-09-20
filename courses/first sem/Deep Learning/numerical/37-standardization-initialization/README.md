# 37. Standardization and initialization scales

Fit and verify training statistics, transform held-out data, handle constants, distinguish pixel scaling, and calculate explicitly optional initializer scales.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture 5 PDF page163 normalization and named initialization methods; Assignment 1 page4 pixel range. numerical-practice.md N6.10. Population-variance convention and optional normal initializer variants explicitly declared.

## Illustrated walkthrough

### 1. Fit preprocessing on training data

![Fit preprocessing on training data](pages/page-01.png)

### 2. Calculate the training mean and deviations

![Calculate the training mean and deviations](pages/page-02.png)

### 3. Calculate variance, then standard deviation

![Calculate variance, then standard deviation](pages/page-03.png)

### 4. Transform all three training values

![Transform all three training values](pages/page-04.png)

### 5. Verify zero mean and unit variance exactly

![Verify zero mean and unit variance exactly](pages/page-05.png)

### 6. Transform a new input without refitting

![Transform a new input without refitting](pages/page-06.png)

### 7. Check the tempting wrong denominator

![Check the tempting wrong denominator](pages/page-07.png)

### 8. Choose a safe policy for a constant feature

![Choose a safe policy for a constant feature](pages/page-08.png)

### 9. Separate standardization from other preprocessing

![Separate standardization from other preprocessing](pages/page-09.png)

### 10. Optional: calculate named initializer scales

![Optional: calculate named initializer scales](pages/page-10.png)

### 11. Take roots before scaling a normal draw

![Take roots before scaling a normal draw](pages/page-11.png)

### 12. Why identical hidden units can stay identical

![Why identical hidden units can stay identical](pages/page-12.png)

### 13. Initialization scope and symmetry

![Initialization scope and symmetry](pages/page-13.png)

### 14. Your turn: fit a fresh training transform

![Your turn: fit a fresh training transform](pages/page-14.png)

### 15. Answer: fresh training mean and spread

![Answer: fresh training mean and spread](pages/page-15.png)

### 16. Answer: every transformed value and held-out input

![Answer: every transformed value and held-out input](pages/page-16.png)

### 17. Answer: optional initializer arithmetic

![Answer: optional initializer arithmetic](pages/page-17.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
