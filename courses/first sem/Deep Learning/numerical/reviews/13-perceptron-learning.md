# 13 Perceptron learning: TA review

## Plan review — APPROVED

L3 p41 +/-1 algorithm, mistakes-only W+=yX with augmented constant and explicit sign0=+1. Fixed data order A(1,0)+1,B(0,1)-1,C(1,1)+1, allzero initialparameters. Show every visit including correct/no-update cases through first full error-free epoch. Boundary plot, tie handling and nonseparable limitation. Independent one-dimensional practice and full two-epoch answer.

Independent simulation: epochends(0,1,0),(0,2,0),(-1,2,-1),same; mistakecounts2,2,1,0. Final Cscore0correct under convention. Practice order(-1,-1),(2,+1), initial(b,w)=(0,-1): bothfirstepochmistakes ->(-1,0)->(0,2), then noerrors. Explain update pushes mistaken point toward label; never stop after single correct point or replace explicit mismatch test with yscore<=0 under asymmetric tie convention.

Final rendered review pending.

## Rendered review — changes requested

All twenty pages plus L3 source p41 visually reviewed. Independently simulated full trace and practice; values correct. Source fidelity, tie rule, immediate updates, full-epoch stopping and plot sound. Required wording: page02 title incorrectly suggests only the mistaken prediction changes; use 'Update only after a mistaken prediction'. Also define squared-length notation on p15 as sum of squared components to aid beginners.

## Final TA verdict — PASS

Re-inspected revised pages02 and15. Title now correctly states the update trigger; squared length is defined in plain language with substituted calculation. All twenty pages have passed visual, independent mathematical, course-fidelity and beginner-understanding review. No blocking findings remain.
