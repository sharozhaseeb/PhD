# 26. RProp: signs, rollback and stored state

Trace every attempted move in the lecture rollback variant, distinguish trial and accepted states, and solve a four-attempt practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture4 PDF pages64-72, especially page71: simplified RProp. Positive-magnitude bounding clarifies signed pseudocode; exact-zero stop convention stated. numerical-practice.md N4.5.

## Illustrated walkthrough

### 1. RProp follows derivative signs and remembers state

![RProp follows derivative signs and remembers state](pages/page-01.png)

### 2. Decide which state is carried to the next attempt

![Decide which state is carried to the next attempt](pages/page-02.png)

### 3. attempt 1: accept and grow

![attempt 1: accept and grow](pages/page-03.png)

### 4. attempt 2: rollback and shrink

![attempt 2: rollback and shrink](pages/page-04.png)

### 5. attempt 3: accept and grow

![attempt 3: accept and grow](pages/page-05.png)

### 6. Why rollback is not a loss-improvement test

![Why rollback is not a loss-improvement test](pages/page-06.png)

### 7. Separate attempted points from accepted history

![Separate attempted points from accepted history](pages/page-07.png)

### 8. Clamp a magnitude, then attach its direction

![Clamp a magnitude, then attach its direction](pages/page-08.png)

### 9. Your turn: four attempts with two reversals

![Your turn: four attempts with two reversals](pages/page-09.png)

### 10. Practice: attempt 1: accept and grow

![Practice: attempt 1: accept and grow](pages/page-10.png)

### 11. Practice: attempt 2: rollback and shrink

![Practice: attempt 2: rollback and shrink](pages/page-11.png)

### 12. Practice: attempt 3: rollback and shrink

![Practice: attempt 3: rollback and shrink](pages/page-12.png)

### 13. Practice: attempt 4: accept and grow

![Practice: attempt 4: accept and grow](pages/page-13.png)

### 14. Practice checkpoint: track accepted state

![Practice checkpoint: track accepted state](pages/page-14.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
