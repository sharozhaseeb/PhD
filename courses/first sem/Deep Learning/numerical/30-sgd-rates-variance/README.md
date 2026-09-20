# 30. SGD rates, work and variance

Step-size sums, bound arithmetic, equal-work comparisons and fully enumerated loss distributions with fresh practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture5 PDF pages40-59,60-74,85-86. Chosen examples follow numerical-practice.md N6.2/N6.3; finite-population correction is a labeled supporting extension.

## Illustrated walkthrough

### 1. Two different questions about SGD

![Two different questions about SGD](pages/page-01.png)

### 2. Read the two infinite-sum conditions

![Read the two infinite-sum conditions](pages/page-02.png)

### 3. Apply the p-series test to both sums

![Apply the p-series test to both sums](pages/page-03.png)

### 4. Check the endpoints instead of guessing

![Check the endpoints instead of guessing](pages/page-04.png)

### 5. Geometric shrinking fails the first sum

![Geometric shrinking fails the first sum](pages/page-05.png)

### 6. Turn an inverse gap bound into an update count

![Turn an inverse gap bound into an update count](pages/page-06.png)

### 7. Solve a geometric bound using logarithms

![Solve a geometric bound using logarithms](pages/page-07.png)

### 8. Fewer updates can still mean more example work

![Fewer updates can still mean more example work](pages/page-08.png)

### 9. Rewrite the mini-batch expression at equal work

![Rewrite the mini-batch expression at equal work](pages/page-09.png)

### 10. Evaluate both terms separately

![Evaluate both terms separately](pages/page-10.png)

### 11. A tiny population of losses

![A tiny population of losses](pages/page-11.png)

### 12. Enumerate every two-draw mini-batch

![Enumerate every two-draw mini-batch](pages/page-12.png)

### 13. See how averaging concentrates probability

![See how averaging concentrates probability](pages/page-13.png)

### 14. Why independent batch variance divides by b

![Why independent batch variance divides by b](pages/page-14.png)

### 15. Calculate variance and standard deviation separately

![Calculate variance and standard deviation separately](pages/page-15.png)

### 16. Without replacement is a different experiment

![Without replacement is a different experiment](pages/page-16.png)

### 17. Optional: finite-population correction

![Optional: finite-population correction](pages/page-17.png)

### 18. Your turn: schedules and bound arithmetic

![Your turn: schedules and bound arithmetic](pages/page-18.png)

### 19. Your turn: a fresh loss distribution

![Your turn: a fresh loss distribution](pages/page-19.png)

### 20. Answer: test each exponent twice

![Answer: test each exponent twice](pages/page-20.png)

### 21. Answer: inverse and geometric counts

![Answer: inverse and geometric counts](pages/page-21.png)

### 22. Answer: equal work and one-draw variability

![Answer: equal work and one-draw variability](pages/page-22.png)

### 23. Answer: four independent draws

![Answer: four independent draws](pages/page-23.png)

### 24. Answer: a full dataset has no sampling uncertainty

![Answer: a full dataset has no sampling uncertainty](pages/page-24.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
