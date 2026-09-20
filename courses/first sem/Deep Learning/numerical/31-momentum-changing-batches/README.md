# 31. Momentum across changing mini-batches

Trace batch gradients and persistent displacement through different data groups and an epoch boundary, with a fresh fully worked practice run.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture 5 PDF pages93-109, specifically103,106,109. Chosen fixed-order numerical-practice.md N6.4 example with an added next-epoch continuation.

## Illustrated walkthrough

### 1. Keep memory when the mini-batch changes

![Keep memory when the mini-batch changes](pages/page-01.png)

### 2. Derive each batch gradient before updating

![Derive each batch gradient before updating](pages/page-02.png)

### 3. Map the lecture equations to our state

![Map the lecture equations to our state](pages/page-03.png)

### 4. Both methods: first A gradient

![Both methods: first A gradient](pages/page-04.png)

### 5. Both methods: first A update

![Both methods: first A update](pages/page-05.png)

### 6. Momentum: B gradient

![Momentum: B gradient](pages/page-06.png)

### 7. Momentum: B update

![Momentum: B update](pages/page-07.png)

### 8. Nesterov: B gradient

![Nesterov: B gradient](pages/page-08.png)

### 9. Nesterov: B update

![Nesterov: B update](pages/page-09.png)

### 10. Continue into a new epoch without resetting state

![Continue into a new epoch without resetting state](pages/page-10.png)

### 11. Momentum: next-epoch A gradient

![Momentum: next-epoch A gradient](pages/page-11.png)

### 12. Momentum: next-epoch A update

![Momentum: next-epoch A update](pages/page-12.png)

### 13. Nesterov: next-epoch A gradient

![Nesterov: next-epoch A gradient](pages/page-13.png)

### 14. Nesterov: next-epoch A update

![Nesterov: next-epoch A update](pages/page-14.png)

### 15. Persistent state versus temporary batch quantities

![Persistent state versus temporary batch quantities](pages/page-15.png)

### 16. Read the three-batch traces together

![Read the three-batch traces together](pages/page-16.png)

### 17. Your turn: change both mini-batches

![Your turn: change both mini-batches](pages/page-17.png)

### 18. Both methods: practice A gradient

![Both methods: practice A gradient](pages/page-18.png)

### 19. Both methods: practice A update

![Both methods: practice A update](pages/page-19.png)

### 20. Momentum: practice B gradient

![Momentum: practice B gradient](pages/page-20.png)

### 21. Momentum: practice B update

![Momentum: practice B update](pages/page-21.png)

### 22. Nesterov: practice B gradient

![Nesterov: practice B gradient](pages/page-22.png)

### 23. Nesterov: practice B update

![Nesterov: practice B update](pages/page-23.png)

### 24. Answer: why resetting memory gives a different result

![Answer: why resetting memory gives a different result](pages/page-24.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
