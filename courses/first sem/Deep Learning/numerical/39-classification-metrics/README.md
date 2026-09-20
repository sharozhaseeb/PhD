# 39. Classification metrics from every prediction

Threshold probabilities, build a labeled confusion matrix, and compute accuracy, precision, recall and F1 with two fully worked practice problems.

[Open the PDF](lesson.pdf)

Lecture reference: Assignment 1 PDF page 4: digit 0 is positive target 1, threshold 0.5, report accuracy, precision, recall, F1 and confusion matrix. Exact tie assigned positive as explicit study convention. numerical-practice.md N5.2.

## Illustrated walkthrough

### 1. Measure whether the model detects digit zero

![Measure whether the model detects digit zero](pages/page-01.png)

### 2. Turn each probability into one class decision

![Turn each probability into one class decision](pages/page-02.png)

### 3. Name the four possible outcomes

![Name the four possible outcomes](pages/page-03.png)

### 4. Classify all eight examples, one row at a time

![Classify all eight examples, one row at a time](pages/page-04.png)

### 5. Collect the counts before computing any metric

![Collect the counts before computing any metric](pages/page-05.png)

### 6. Read the confusion matrix with its axes

![Read the confusion matrix with its axes](pages/page-06.png)

### 7. Accuracy: what fraction of all decisions is correct?

![Accuracy: what fraction of all decisions is correct?](pages/page-07.png)

### 8. Precision: how reliable are positive predictions?

![Precision: how reliable are positive predictions?](pages/page-08.png)

### 9. Recall: what fraction of actual zeros is detected?

![Recall: what fraction of actual zeros is detected?](pages/page-09.png)

### 10. F1: combine precision and recall

![F1: combine precision and recall](pages/page-10.png)

### 11. Compute the same F1 directly from counts

![Compute the same F1 directly from counts](pages/page-11.png)

### 12. The same accuracy can hide a failed detector

![The same accuracy can hide a failed detector](pages/page-12.png)

### 13. Handle empty denominators explicitly

![Handle empty denominators explicitly](pages/page-13.png)

### 14. Your turn: include the exact threshold tie

![Your turn: include the exact threshold tie](pages/page-14.png)

### 15. Answer: threshold, compare, then count

![Answer: threshold, compare, then count](pages/page-15.png)

### 16. Answer: matrix and accuracy

![Answer: matrix and accuracy](pages/page-16.png)

### 17. Answer: precision, recall and F1

![Answer: precision, recall and F1](pages/page-17.png)

### 18. A second quiz: start from supplied counts

![A second quiz: start from supplied counts](pages/page-18.png)

### 19. Answer: supplied counts to all four metrics

![Answer: supplied counts to all four metrics](pages/page-19.png)

### 20. A reliable exam workflow

![A reliable exam workflow](pages/page-20.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
