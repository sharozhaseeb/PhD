# 20. A complete two-example batch update

Derive both-example gradients, average and update all fifteen parameters, and recompute both full forwards and losses; includes a fresh full-network practice batch.

[Open the PDF](lesson.pdf)

Lecture reference: Backpropagation_Derivation.pdf pages 2-3; Assignment 1.pdf mean BCE and backpropagation; numerical-practice.md N3.5.

## Illustrated walkthrough

### 1. One batch means one common starting state

![One batch means one common starting state](pages/page-01.png)

### 2. Per-example loss first; mean loss second

![Per-example loss first; mean loss second](pages/page-02.png)

### 3. Original forward values and starting cost

![Original forward values and starting cost](pages/page-03.png)

### 4. B: start backward at the output

![B: start backward at the output](pages/page-04.png)

### 5. B: hidden layer 2, neuron 1 delta

![B: hidden layer 2, neuron 1 delta](pages/page-05.png)

### 6. B: hidden layer 2, neuron 2 delta

![B: hidden layer 2, neuron 2 delta](pages/page-06.png)

### 7. B: hidden layer 1, neuron 1 delta

![B: hidden layer 1, neuron 1 delta](pages/page-07.png)

### 8. B: hidden layer 1, neuron 2 delta

![B: hidden layer 1, neuron 2 delta](pages/page-08.png)

### 9. B: layer 1, neuron 1 gradients

![B: layer 1, neuron 1 gradients](pages/page-09.png)

### 10. B: layer 1, neuron 2 gradients

![B: layer 1, neuron 2 gradients](pages/page-10.png)

### 11. B: layer 2, neuron 1 gradients

![B: layer 2, neuron 1 gradients](pages/page-11.png)

### 12. B: layer 2, neuron 2 gradients

![B: layer 2, neuron 2 gradients](pages/page-12.png)

### 13. B: layer 3, neuron 1 gradients

![B: layer 3, neuron 1 gradients](pages/page-13.png)

### 14. update layer 1, neuron 1

![update layer 1, neuron 1](pages/page-14.png)

### 15. update layer 1, neuron 2

![update layer 1, neuron 2](pages/page-15.png)

### 16. update layer 2, neuron 1

![update layer 2, neuron 1](pages/page-16.png)

### 17. update layer 2, neuron 2

![update layer 2, neuron 2](pages/page-17.png)

### 18. update layer 3, neuron 1

![update layer 3, neuron 1](pages/page-18.png)

### 19. fresh A, layer 1

![fresh A, layer 1](pages/page-19.png)

### 20. fresh A, layer 2

![fresh A, layer 2](pages/page-20.png)

### 21. fresh A, layer 3

![fresh A, layer 3](pages/page-21.png)

### 22. fresh B, layer 1

![fresh B, layer 1](pages/page-22.png)

### 23. fresh B, layer 2

![fresh B, layer 2](pages/page-23.png)

### 24. fresh B, layer 3

![fresh B, layer 3](pages/page-24.png)

### 25. compare the new batch mean

![compare the new batch mean](pages/page-25.png)

### 26. Your turn: a fresh complete training step

![Your turn: a fresh complete training step](pages/page-26.png)

### 27. C: original forward, layer 1

![C: original forward, layer 1](pages/page-27.png)

### 28. C: original forward, layer 2

![C: original forward, layer 2](pages/page-28.png)

### 29. C: original forward, layer 3

![C: original forward, layer 3](pages/page-29.png)

### 30. C: output delta

![C: output delta](pages/page-30.png)

### 31. C: hidden layer 2, neuron 1 delta

![C: hidden layer 2, neuron 1 delta](pages/page-31.png)

### 32. C: hidden layer 2, neuron 2 delta

![C: hidden layer 2, neuron 2 delta](pages/page-32.png)

### 33. C: hidden layer 1, neuron 1 delta

![C: hidden layer 1, neuron 1 delta](pages/page-33.png)

### 34. C: hidden layer 1, neuron 2 delta

![C: hidden layer 1, neuron 2 delta](pages/page-34.png)

### 35. C: layer 1, neuron 1 gradients

![C: layer 1, neuron 1 gradients](pages/page-35.png)

### 36. C: layer 1, neuron 2 gradients

![C: layer 1, neuron 2 gradients](pages/page-36.png)

### 37. C: layer 2, neuron 1 gradients

![C: layer 2, neuron 1 gradients](pages/page-37.png)

### 38. C: layer 2, neuron 2 gradients

![C: layer 2, neuron 2 gradients](pages/page-38.png)

### 39. C: layer 3, neuron 1 gradients

![C: layer 3, neuron 1 gradients](pages/page-39.png)

### 40. D: original forward, layer 1

![D: original forward, layer 1](pages/page-40.png)

### 41. D: original forward, layer 2

![D: original forward, layer 2](pages/page-41.png)

### 42. D: original forward, layer 3

![D: original forward, layer 3](pages/page-42.png)

### 43. D: output delta

![D: output delta](pages/page-43.png)

### 44. D: hidden layer 2, neuron 1 delta

![D: hidden layer 2, neuron 1 delta](pages/page-44.png)

### 45. D: hidden layer 2, neuron 2 delta

![D: hidden layer 2, neuron 2 delta](pages/page-45.png)

### 46. D: hidden layer 1, neuron 1 delta

![D: hidden layer 1, neuron 1 delta](pages/page-46.png)

### 47. D: hidden layer 1, neuron 2 delta

![D: hidden layer 1, neuron 2 delta](pages/page-47.png)

### 48. D: layer 1, neuron 1 gradients

![D: layer 1, neuron 1 gradients](pages/page-48.png)

### 49. D: layer 1, neuron 2 gradients

![D: layer 1, neuron 2 gradients](pages/page-49.png)

### 50. D: layer 2, neuron 1 gradients

![D: layer 2, neuron 1 gradients](pages/page-50.png)

### 51. D: layer 2, neuron 2 gradients

![D: layer 2, neuron 2 gradients](pages/page-51.png)

### 52. D: layer 3, neuron 1 gradients

![D: layer 3, neuron 1 gradients](pages/page-52.png)

### 53. Practice: initial mean loss

![Practice: initial mean loss](pages/page-53.png)

### 54. Practice: update layer 1, neuron 1

![Practice: update layer 1, neuron 1](pages/page-54.png)

### 55. Practice: update layer 1, neuron 2

![Practice: update layer 1, neuron 2](pages/page-55.png)

### 56. Practice: update layer 2, neuron 1

![Practice: update layer 2, neuron 1](pages/page-56.png)

### 57. Practice: update layer 2, neuron 2

![Practice: update layer 2, neuron 2](pages/page-57.png)

### 58. Practice: update layer 3, neuron 1

![Practice: update layer 3, neuron 1](pages/page-58.png)

### 59. C: updated forward, layer 1

![C: updated forward, layer 1](pages/page-59.png)

### 60. C: updated forward, layer 2

![C: updated forward, layer 2](pages/page-60.png)

### 61. C: updated forward, layer 3

![C: updated forward, layer 3](pages/page-61.png)

### 62. D: updated forward, layer 1

![D: updated forward, layer 1](pages/page-62.png)

### 63. D: updated forward, layer 2

![D: updated forward, layer 2](pages/page-63.png)

### 64. D: updated forward, layer 3

![D: updated forward, layer 3](pages/page-64.png)

### 65. Practice: refreshed mean and readiness check

![Practice: refreshed mean and readiness check](pages/page-65.png)

### 66. Checks that prevent common batch mistakes

![Checks that prevent common batch mistakes](pages/page-66.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
