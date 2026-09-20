# 38. Early stopping, selection, bagging and augmentation

Trace every checkpoint and patience decision, restore the correct model, count experimental runs, and distinguish training-data bagging from augmentation.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture 5 pages145-149 bagging,160 early stopping,162 augmentation,164 setup. numerical-practice.md N6.11. Patience2 and min_delta0 are chosen exercise rules, not supplied pseudocode.

## Illustrated walkthrough

### 1. Choose when to stop and what to restore

![Choose when to stop and what to restore](pages/page-01.png)

### 2. State the rule before reading future losses

![State the rule before reading future losses](pages/page-02.png)

### 3. Read the supplied training and validation history

![Read the supplied training and validation history](pages/page-03.png)

### 4. Epochs 1 and 2: save improvements

![Epochs 1 and 2: save improvements](pages/page-04.png)

### 5. Epochs 3 and 4: fail, then reset

![Epochs 3 and 4: fail, then reset](pages/page-05.png)

### 6. Epochs 5 and 6: patience is exhausted

![Epochs 5 and 6: patience is exhausted](pages/page-06.png)

### 7. See stopping and restoration as different events

![See stopping and restoration as different events](pages/page-07.png)

### 8. Restore the model, not just a recorded score

![Restore the model, not just a recorded score](pages/page-08.png)

### 9. Count hyperparameter settings and seeded runs

![Count hyperparameter settings and seeded runs](pages/page-09.png)

### 10. Bagging: sample training data for several models

![Bagging: sample training data for several models](pages/page-10.png)

### 11. Declare how the ensemble combines predictions

![Declare how the ensemble combines predictions](pages/page-11.png)

### 12. Augmentation: split originals before creating variants

![Augmentation: split originals before creating variants](pages/page-12.png)

### 13. Count items, not independent originals

![Count items, not independent originals](pages/page-13.png)

### 14. Your turn: equality and an unobserved future value

![Your turn: equality and an unobserved future value](pages/page-14.png)

### 15. Answer: equality does not reset patience

![Answer: equality does not reset patience](pages/page-15.png)

### 16. Answer: configurations, votes and variants

![Answer: configurations, votes and variants](pages/page-16.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
