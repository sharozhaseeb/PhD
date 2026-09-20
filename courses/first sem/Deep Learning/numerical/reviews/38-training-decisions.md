# Lesson 38 TA review

## Plan discussion — approved

Use a precise chosen policy: lower validation loss is better, min_delta=0, strict decrease only, equality is failure, patience two consecutive failures. Save each improvement and restore best observed checkpoint. Main stop epoch 6/restore 4; fresh sequence stops 4/restores 2, and supplied epoch 5 is hypothetical and unobserved. This avoids ambiguity between meaningful and absolute-best improvements. Define model checkpoint, validation selection and untouched final test. Grid/seed counts, training-only bootstrap bagging and distinct majority/probability aggregation, and split-before-augmentation counts receive complete fresh answers. Source algorithms versus chosen conventions must remain explicit.

Final rendered review pending.

## Final TA verdict — PASS

Reviewed all 16 rendered pages and actual Lecture 5 source pages 145, 160, 162 and 164. Revised page 16 rechecked: the 40 originals are explicitly the training partition after splitting the original dataset, preserving the 160-item calculation. Diagrams, tables and plot are clear with no overlap.

Independent sequential Python simulation confirmed every best-loss/counter/checkpoint state: main stop 6, restore 4; fresh stop 4, restore 2, with epoch 5 unobserved. Independently checked 12 settings/36 seeded runs, fresh 24 runs, mean probability 1.9/3, majority votes and 300/160 augmented-item counts.

Student/source fidelity: chosen strict min_delta=0 rule includes equality as failure and one common checkpoint/patience reference. Parameters rather than loss numbers are restored; optimizer state is distinguished for resumed training. Test data remain outside selection. Bootstrap replacement, separate models and aggregation alternatives are explained. Original-first partitioning, label preservation and dependent augmented siblings prevent misleading sample-count claims. Full independent practice has separate worked answers.
