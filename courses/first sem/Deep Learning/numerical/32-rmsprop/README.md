# 32. RMSProp, one coordinate at a time

Calculate ordinary RMS, distinguish second moments from variance, and trace two complete two-parameter RMSProp updates with fresh practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture 5 PDF pages110-118, coordinate sequence114, recurrence116 and mini-batch algorithm118. numerical-practice.md N6.5 supplied-gradient examples; arithmetic-only epsilon0 plus a positive-epsilon comparison.

## Illustrated walkthrough

### 1. Start with root mean square

![Start with root mean square](pages/page-01.png)

### 2. RMS of the horizontal coordinate sequence

![RMS of the horizontal coordinate sequence](pages/page-02.png)

### 3. RMS of the vertical coordinate sequence

![RMS of the vertical coordinate sequence](pages/page-03.png)

### 4. RMS is different from standard deviation

![RMS is different from standard deviation](pages/page-04.png)

### 5. The course RMSProp recurrence

![The course RMSProp recurrence](pages/page-05.png)

### 6. Average the current batch before squaring

![Average the current batch before squaring](pages/page-06.png)

### 7. Set up the two-coordinate optimizer exercise

![Set up the two-coordinate optimizer exercise](pages/page-07.png)

### 8. update 1, coordinate 1

![update 1, coordinate 1](pages/page-08.png)

### 9. update 1, coordinate 2

![update 1, coordinate 2](pages/page-09.png)

### 10. update 2, coordinate 1

![update 2, coordinate 1](pages/page-10.png)

### 11. update 2, coordinate 2

![update 2, coordinate 2](pages/page-11.png)

### 12. Read the vector states together

![Read the vector states together](pages/page-12.png)

### 13. Expand the memory to see its weights

![Expand the memory to see its weights](pages/page-13.png)

### 14. Positive epsilon changes the denominator

![Positive epsilon changes the denominator](pages/page-14.png)

### 15. Why a stabilizer matters at zero

![Why a stabilizer matters at zero](pages/page-15.png)

### 16. Your turn: a fresh sign-changing coordinate

![Your turn: a fresh sign-changing coordinate](pages/page-16.png)

### 17. Practice: update 1, coordinate 1

![Practice: update 1, coordinate 1](pages/page-17.png)

### 18. Practice: update 1, coordinate 2

![Practice: update 1, coordinate 2](pages/page-18.png)

### 19. Practice: update 2, coordinate 1

![Practice: update 2, coordinate 1](pages/page-19.png)

### 20. Practice: update 2, coordinate 2

![Practice: update 2, coordinate 2](pages/page-20.png)

### 21. Practice checkpoint and common mistakes

![Practice checkpoint and common mistakes](pages/page-21.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
