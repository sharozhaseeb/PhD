# 25. Learning-rate schedules and indexing

Substitute every schedule index, apply changing rates to gradient descent, trace a plateau rule, and solve fresh practice.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture4 PDF page57: reciprocal-linear, reciprocal-quadratic, exponential and stagnation-triggered multiplicative decay. numerical-practice.md N4.4; precise plateau counter is a labeled study extension.

## Illustrated walkthrough

### 1. Read the exact schedule and its index

![Read the exact schedule and its index](pages/page-01.png)

### 2. Reciprocal linear: substitute k before dividing

![Reciprocal linear: substitute k before dividing](pages/page-02.png)

### 3. Reciprocal quadratic: square the whole denominator

![Reciprocal quadratic: square the whole denominator](pages/page-03.png)

### 4. Exponential: use the logarithm identity

![Exponential: use the logarithm identity](pages/page-04.png)

### 5. Compare the first four scheduled rates

![Compare the first four scheduled rates](pages/page-05.png)

### 6. See the rates over more update indices

![See the rates over more update indices](pages/page-06.png)

### 7. Apply the rate with the matching current gradient

![Apply the rate with the matching current gradient](pages/page-07.png)

### 8. A plateau rule responds to measured progress

![A plateau rule responds to measured progress](pages/page-08.png)

### 9. Trace the plateau decision at every epoch

![Trace the plateau decision at every epoch](pages/page-09.png)

### 10. Your turn: new initial rate and decay constant

![Your turn: new initial rate and decay constant](pages/page-10.png)

### 11. Practice: rates and the next parameter

![Practice: rates and the next parameter](pages/page-11.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
