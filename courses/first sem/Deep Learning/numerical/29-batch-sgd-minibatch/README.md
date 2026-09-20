# 29. Full batch, SGD and mini-batches

Trace identical data through different update groupings and orders, report the full objective, count remainder batches, and solve fresh practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture5 PDF pages6-39: batch/incremental/SGD; pages77-82: mini-batch, especially algorithm page82. numerical-practice.md N6.1; fixed rate and retained partial batch explicitly stated.

## Illustrated walkthrough

### 1. Keep the model simple to isolate batching

![Keep the model simple to isolate batching](pages/page-01.png)

### 2. Examples, batches, updates and epochs

![Examples, batches, updates and epochs](pages/page-02.png)

### 3. Full batch, update 1

![Full batch, update 1](pages/page-03.png)

### 4. SGD forward, update 1

![SGD forward, update 1](pages/page-04.png)

### 5. SGD forward, update 2

![SGD forward, update 2](pages/page-05.png)

### 6. SGD forward, update 3

![SGD forward, update 3](pages/page-06.png)

### 7. SGD forward, update 4

![SGD forward, update 4](pages/page-07.png)

### 8. SGD reverse, update 1

![SGD reverse, update 1](pages/page-08.png)

### 9. SGD reverse, update 2

![SGD reverse, update 2](pages/page-09.png)

### 10. SGD reverse, update 3

![SGD reverse, update 3](pages/page-10.png)

### 11. SGD reverse, update 4

![SGD reverse, update 4](pages/page-11.png)

### 12. Mini-batch, update 1

![Mini-batch, update 1](pages/page-12.png)

### 13. Mini-batch, update 2

![Mini-batch, update 2](pages/page-13.png)

### 14. Same epoch, different sequences of parameter states

![Same epoch, different sequences of parameter states](pages/page-14.png)

### 15. Compare paths by examples processed

![Compare paths by examples processed](pages/page-15.png)

### 16. Report the full objective at the final parameter

![Report the full objective at the final parameter](pages/page-16.png)

### 17. Count updates and retain the last partial batch

![Count updates and retain the last partial batch](pages/page-17.png)

### 18. Your turn: fresh targets and a different rate

![Your turn: fresh targets and a different rate](pages/page-18.png)

### 19. Practice: Full batch, update 1

![Practice: Full batch, update 1](pages/page-19.png)

### 20. Practice: SGD forward, update 1

![Practice: SGD forward, update 1](pages/page-20.png)

### 21. Practice: SGD forward, update 2

![Practice: SGD forward, update 2](pages/page-21.png)

### 22. Practice: SGD reverse, update 1

![Practice: SGD reverse, update 1](pages/page-22.png)

### 23. Practice: SGD reverse, update 2

![Practice: SGD reverse, update 2](pages/page-23.png)

### 24. Practice checkpoint and remainder calculation

![Practice checkpoint and remainder calculation](pages/page-24.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
