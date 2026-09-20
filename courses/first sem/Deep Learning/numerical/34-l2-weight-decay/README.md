# 34. L2 regularization and weight decay

Compute every loss and gradient term, update all parameters, check the full new objective, and reconcile the lecture shrink-factor notation.

[Open the PDF](lesson.pdf)

Lecture reference: Lecture 5 pages125-143; objective137, update138, sigmoid steepness133. numerical-practice.md N6.7. Bias exclusion is an explicitly chosen exercise convention.

## Illustrated walkthrough

### 1. Add a cost for large selected weights

![Add a cost for large selected weights](pages/page-01.png)

### 2. Set up the main three-parameter example

![Set up the main three-parameter example](pages/page-02.png)

### 3. Compute prediction and data loss

![Compute prediction and data loss](pages/page-03.png)

### 4. Compute the penalty and total objective

![Compute the penalty and total objective](pages/page-04.png)

### 5. Differentiate each part of the objective

![Differentiate each part of the objective](pages/page-05.png)

### 6. Substitute every main gradient

![Substitute every main gradient](pages/page-06.png)

### 7. Update all three parameters simultaneously

![Update all three parameters simultaneously](pages/page-07.png)

### 8. Check the new full regularized objective

![Check the new full regularized objective](pages/page-08.png)

### 9. Derive the weight-decay form algebraically

![Derive the weight-decay form algebraically](pages/page-09.png)

### 10. Verify both weight updates using the shrink factor

![Verify both weight updates using the shrink factor](pages/page-10.png)

### 11. Read the boxed lecture factor carefully

![Read the boxed lecture factor carefully](pages/page-11.png)

### 12. Why Adam needs a separate distinction

![Why Adam needs a separate distinction](pages/page-12.png)

### 13. Relate a scalar weight to input sensitivity

![Relate a scalar weight to input sensitivity](pages/page-13.png)

### 14. See the two scalar sigmoid responses

![See the two scalar sigmoid responses](pages/page-14.png)

### 15. Your turn: fresh data, weights and regularization

![Your turn: fresh data, weights and regularization](pages/page-15.png)

### 16. Answer: prediction and both loss terms

![Answer: prediction and both loss terms](pages/page-16.png)

### 17. Answer: every practice gradient and update

![Answer: every practice gradient and update](pages/page-17.png)

### 18. Answer: verify the factor and recompute prediction

![Answer: verify the factor and recompute prediction](pages/page-18.png)

### 19. Answer: the new full objective

![Answer: the new full objective](pages/page-19.png)

Original study example. Read the practice question before revealing the following answer pages.

[Back to numerical index](../README.md)
