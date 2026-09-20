# 36. Coordinate and global-norm gradient clipping

Work the slide ceiling and two signed-gradient extensions, compare vector directions and updates, handle zero, and solve fresh clipping practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture 5 PDF page 161 gives the one-sided positive ceiling. Symmetric coordinate and global L2-norm clipping are explicitly labeled supporting extensions; numerical-practice.md N6.9.

## Illustrated walkthrough

### 1. Clip a gradient before using it in an update

![Clip a gradient before using it in an update](pages/page-01.png)

### 2. Work the slide one-sided ceiling literally

![Work the slide one-sided ceiling literally](pages/page-02.png)

### 3. Symmetric coordinate clipping

![Symmetric coordinate clipping](pages/page-03.png)

### 4. Global norm clipping: measure the vector length

![Global norm clipping: measure the vector length](pages/page-04.png)

### 5. Use the norm-clipped vector in the update

![Use the norm-clipped vector in the update](pages/page-05.png)

### 6. A component cap is not a length cap

![A component cap is not a length cap](pages/page-06.png)

### 7. See the directions and allowed regions

![See the directions and allowed regions](pages/page-07.png)

### 8. Compare the resulting parameter states

![Compare the resulting parameter states](pages/page-08.png)

### 9. Handle a small vector, a boundary and zero

![Handle a small vector, a boundary and zero](pages/page-09.png)

### 10. Your turn: a large negative component

![Your turn: a large negative component](pages/page-10.png)

### 11. Answer: one-sided and symmetric coordinate rules

![Answer: one-sided and symmetric coordinate rules](pages/page-11.png)

### 12. Answer: norm, scale and clipped components

![Answer: norm, scale and clipped components](pages/page-12.png)

### 13. Answer: the final norm-clipped update

![Answer: the final norm-clipped update](pages/page-13.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
