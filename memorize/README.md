# Memorize

An optimal algorithm for spaced repetition

# Introduction

It is well known that repeated and spaced reviews of knowledge is neccessary for improving retention. However, it is unclear what is best schedule for reviewing. Several heuristics have been suggested, but they lack guarantees of optimality. In this work, we will describe a way of coming up with an optimal scheduling algorithm which we name Memorize.

# Problem setup

Let us consider the problem of learning _one_ knowledge item. We assume that we know how _difficult_ learning the item is. Our algorithm will determine the time the item is to be reviewed by the learner. The learner will be _tested_ at that time to see if he can recall the item and our algorithm will update our next-reviewing time based on that information, _adapting_ to the user.

The objective of the algorithm is to keep the recall of the item high during the experiment duration ![(0, T)](https://render.githubusercontent.com/render/math?math=(0%2C%20T)) while minimizing the total number of reviews that the learner has to do.

# Memory models

Before we can start talking about scheduling, we need a model of human memory, which can help us predict how humans forget. There are multiple models of memory which can predict the probability of recall at time _t_ given the past reviews of the item and its _difficulty_.

![memory-model](https://learning.mpi-sws.org/memorize/img/memory-model.png)

We will assume that the probability of recall follows the analytically simple exponential forgetting curve model. In our paper, we have extended the analysis to more widely accepted power-law forgetting curve model of memory as well.

In the exponential forgetting curve model of memory, we assume that probability of recall _m(t)_ of the item immediately after a review is 1. Then, as the name suggests, the probability of recall _m(t)_ decays exponentially with a forgetting rate _n(t)_, which depends on the past reviews and the item difficulty:

![m(t) = e^{-n(t)(t-t_{\text{last review}})}](https://render.githubusercontent.com/render/math?math=m(t)%20%3D%20e%5E%7B-n(t)(t-t_%7B%5Ctext%7Blast%20review%7D%7D)%7D)


Our estimate of the forgetting rate is adapted to be higher or lower depending on whether the learner managed to recall the item at a review or not:

![n(t + dt) = \begin{cases} (1 - \alpha) \times n(t) & \text{if item was recalled}\\ (1 + \beta) \times n(t) & \text{if item was forgotten} \end{cases}](https://render.githubusercontent.com/render/math?math=n(t%20%2B%20dt)%20%3D%20%5Cbegin%7Bcases%7D%20(1%20-%20%5Calpha)%20%5Ctimes%20n(t)%20%26%20%5Ctext%7Bif%20item%20was%20recalled%7D%5C%5C%20(1%20%2B%20%5Cbeta)%20%5Ctimes%20n(t)%20%26%20%5Ctext%7Bif%20item%20was%20forgotten%7D%20%5Cend%7Bcases%7D)

![\alpha](https://render.githubusercontent.com/render/math?math=%5Calpha) and ![\beta](https://render.githubusercontent.com/render/math?math=%5Cbeta), as well as the initial difficulty ![n(0)](https://render.githubusercontent.com/render/math?math=n(0)), are parameters of the model which are derived from the dataset using a variant of Halflife regression.