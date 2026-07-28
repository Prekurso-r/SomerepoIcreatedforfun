# Traffic — Experimentation Process

The task is to classify 30x30 RGB images of German traffic signs into 43
categories. I started from the simplest thing that could possibly work and added
one idea at a time, keeping everything else fixed so each change was measurable.

All numbers below come from the full `gtsrb` dataset (26,640 images), the same
fixed 60/40 train/test split (`random_state=42`), and 10 epochs of `adam` on
categorical cross-entropy. Accuracy is on the held-out test set.

## What I tried

| # | Architecture | Test acc. | Test loss | Params |
|---|---|---|---|---|
| 0 | no convolution: flatten → dense 128 | 0.8934 | 0.4446 | 351,275 |
| 1 | one conv block (32 filters) → dense 128 | 0.9661 | 0.1572 | 809,387 |
| 2 | two conv blocks (32, 64) → dense 128, no dropout | 0.9770 | 0.0943 | 319,979 |
| 3 | two conv blocks (32, 64) → dense 128 + dropout 0.5 | 0.9853 | 0.0676 | 319,979 |
| 4 | two conv blocks (32, 64) → dense 128 + dropout 0.2 | 0.9898 | 0.0499 | 319,979 |
| 5 | three conv blocks (32, 64, 128) → dense 128 + dropout 0.5 | 0.9873 | 0.0489 | 164,459 |
| 6 | two conv blocks (32, 64) → dense 512 + dropout 0.5 | 0.9899 | 0.0466 | 1,221,611 |
| 7 | two conv blocks (32, 64) → two dense 128 + dropout 0.5 | 0.9564 | 0.1661 | 336,491 |

A "conv block" is `Conv2D(n, 3x3, relu)` followed by `MaxPooling2D(2x2)`. Every
model begins with a `Rescaling(1/255)` layer and ends with a 43-unit softmax.

## What I learned

**Convolution is where almost all the accuracy comes from.** A plain dense
network (#0) already reaches 89%, which sounds respectable until you compare it
to 96.6% from adding a *single* convolutional block (#1). Traffic signs are
defined by shape and local pattern — a triangle border, a digit, an arrow — and
a dense layer over raw pixels has to learn each of those separately for every
position in the image. A convolutional filter learns it once.

**A second convolutional block helped and made the model smaller.** Going from
one block to two (#1 → #2) raised accuracy from 96.6% to 97.7% *and* cut the
parameter count from 809k to 320k, because the extra pooling step shrinks the
feature map before it reaches the flatten layer. That was the most satisfying
result of the whole process: a strictly better model for a third of the weights.
A third block (#5) kept shrinking the model (164k params) but no longer improved
accuracy, so the depth had stopped paying for itself at that image size — 30x30
does not survive many halvings.

**Dropout fixed a real overfitting gap.** Without it (#2) the model finished at
99.1% training accuracy but only 97.7% on test — it was memorising. Adding
dropout 0.5 (#3) closed most of that gap. Interestingly, the final *training*
accuracy with dropout 0.5 dropped to 92.3% while test accuracy went **up**,
which is exactly what you want to see: the model is no longer scoring points on
the training set it can't reproduce on unseen images.

**More than one hidden dense layer hurt badly.** Stacking two 128-unit dense
layers each behind dropout 0.5 (#7) was the worst change I made — 95.6%, well
below the single-layer version. Dropping half the units twice in a row starves
the second layer; 10 epochs isn't enough for it to recover. The lesson was that
dropout is not free, and depth in the classifier head is not the same kind of
win as depth in the convolutional stack.

## Choosing the final model

Configurations #4, #5 and #6 all landed within 0.3 points of each other, which
is close enough that a single run couldn't distinguish them. I re-ran the top
four across three random seeds:

| Architecture | mean | min | max |
|---|---|---|---|
| #6 two conv → dense 512 + dropout 0.5 | **0.9913** | 0.9906 | 0.9922 |
| #5 three conv → dense 128 + dropout 0.5 | 0.9875 | 0.9869 | 0.9884 |
| #3 two conv → dense 128 + dropout 0.5 | 0.9855 | 0.9834 | 0.9876 |
| #4 two conv → dense 128 + dropout 0.2 | 0.9853 | 0.9794 | 0.9898 |

This settled it. #6 was not just ahead on average — its *worst* run (99.06%)
beat every other configuration's *best* run. The apparent tie between #4 and #6
in the single-run table was noise: #4 swings by a full point across seeds
(97.94% to 98.98%), while #6 varies by less than 0.2. The wider dense layer
gives the classifier enough capacity to use the convolutional features, and
dropout 0.5 keeps that capacity from turning into memorisation.

**Final model:** rescale → conv 32 → pool → conv 64 → pool → flatten →
dense 512 → dropout 0.5 → dense 43 (softmax), reaching roughly **99.1%** test
accuracy.
