# Half-Life Regression

Half-life regression (HLR) is a model for spaced repetition practice, with particular applications to second language acquisition. The model marries psycholinguistic theory with modern machine learning techniques, indirectly estimating the "half-life" of words (and potentially any other item or fact) in a student's long-term memory.

# Abtract

We present _half-life regression_ (HLR), a novel model for spaced repetition practice with applications to second language acquisition. HLR combines psycholinguistic theory with modern machine learning techniques, indirectly estimating the "half-life" of a word or concept in a student's long-term memory. We use data from Duolingo - a popular online language learning application - to fit HLR models, reducing error by 45%+ compared to several baselines at predicting student recal rates. HLR model weights also shed light on which linguistic concepts are systematically challenging for second language learners. Finally, HLR was able to improve Duolingo daily student engagement by 12% in an operational user study.

# Introduction

The _spacing effect_ is the observation that people tend to remember things more effictively if they use _spaced repetition practice_ (short study periods spread out over time) as opposed to _massed practice_ (i.e. "cramming"). The phenomenon was first documented by Ebbinghaus (1885), using himself as a subject in several experiments to memorize verbal utterances. In one study, after a day of cramming he could accurately recite 12-syllable sequences (of gibberish, apparently). However, he could achieve comparable results with half as many practices spread out over three days.

The _lag effect_ (Melton, 1970) is the related observation that people learn even better if the spacing between gradually increases. For example, a learning schedule might begin with review sessions a few second apart, then minutes, then hours, days, months, and so on, with each successive review stretching out over a longer and longer time interval.

The effects of spacing and lag are well-established in second language acquisition research (Atkinson, 1972; Bloom and Shuell, 1981; Cepeda et al., 2006; Pavlik Jr and Anderson, 2008), and benefits have also been shown for gymnastics, baseball pitching, video games, and many other skills. See Ruth (1928), Dempster (1989), and Donovan and Radosevich (1999) for thorough meta-analyses spanning several decades.

Most practical algorithms for spaced repetition are simple functions with a few hand-picked parameters. This is reasonable, since they were largely developed during the 1960s-80s, when people would had to manage practice schedules without the aid of computers. However, the recent popularity of large-scale online learning software makes it possible to collect vast amounts of parallel student data, which can be used to empirically train richer statistical models.

In this work, we propose _half-life regression_ (HLR) as a trainable spaced repetition algorithm, marrying psycholinguistically-inspired models of memory with modern machine learning techniques. We apply this model to real student learning data from Duolingo, a popular language learning app, and use it to improve its large scale, operational, personalized learning system.

# Duolingo

Duolingo is a free, award-winning, online language learning platform. Since launching in 2012, more than 150 million students from all over the world have enrolled in a Duolingo course, either via the website or mobile apps for Android, iOS, and Windows devices. For comparision, that is more than the total number of students in U.S. elementary and secondary school combined. At least 80 language courses are currently available or under development for the Doulingo platform. The most popular courses are for learning English, Spanish, French, and German, although there are also courses for minority languages (Irish Gaelic), and even constructed languages (Esperanto).

More than half of Duolingo students live in developing countries, where Internet access has more than tripled in the past three years (ITU and UNESCO, 2015). The majority of these students are using Duolingo to learn English, which can significantly improve their job prospects and quality of life (Pinon and Haydon, 2010).

## System Overview

Duolingo uses a playfully illustrated, gamified design that combines point-reward incentives with implicit instruction (DeKeyser, 2008), mastery learning (Block et al. 1971), explanations (Fahy, 2004), and other best practices. Early research suggests that 34 hours of Duolingo is equivalent to a full semeter of university-level Spanish instruction (Vesselinov and Grego, 2012).

Figure 1(a) shows and example __skill tree__ for English speakers learning French. This specifies the game-like curriculum: each icon represents a __skill__, which in turn teaches a set of thematically or grammatically related words or concepts. Students tap an icon to access lessons of new material, or to practice previously-learned material. Figure 1(b) shows a screen for the French skill _Gerund_, which teches common gerund verb forms such as _faisant_ (doing) and _etant_ (being). This skill, as well as several others, have already been completed by the student. However, the _Measures_ skill in the bottom right of Figure 1(a) has one lesson remaining. After completing each row of skills, students "unlock" the next row of more advanced skills. This is a gamelike implementation of _mastery learning_, whereby student must reach a certain level of prerequisite knowledge before moving on the new material.

Each language course also contains a __corpus__ (large database of available exercises) and a __lexeme tagger__ (statistical NLP pipeline for automatically tagging and indexing the corpus; see the Appendix for details and a lexeme tag reference). Figure 1(c,d) shows and example translation exercise that might appear in the _Gerund_ skill, and Figure 2 shows the lexeme tagger output for this sentance. Since this exercise is indexed with a gerund lexeme tag (etre.V.GER in this case), it is available for lessons or practices in this skill.

The lexeme tagger also helps to provide corrective feedback. Educational researchers maintain that incorrect answers should be accompanied by _explanations_, not simply a "wrong" mark (Fahy, 2004). In Figure 1(d), the student incorrectly used the 2nd-person verb form _es_ (etre.V.PRES.P2.SG) instead of the 3rd-person _est_ (etre.V.PRES.P3.SG). If Duolingo is able to parse the student response and detect a known grammatical  mistake such as this, it provides and explanation in plain language. Each lesson continues until the student masters all of the __target words__ being taught in the session, as estimated by a mixture model of short-term learning curves (Streeter, 2015).

## Spaced Repetition and Practice

Once a lesson is completed, all the target words being taught in the lesson are added to the __student model__. This model captures what the student has learned, and estimates how well she can recall this knowledge at any given time. Spaced repetition is a key component of the student model: over time, the strength of a skill decay in the student's long-term memory, and this model helps the student manage her practice schedule.

Duolingo uses __strength meters__ to visualize the student model, as seen beneath each of the completed skill icons in Figure 1(a). These meters represent the average probability that the student can, at any moment, correctly recall a random target word from the lessons in this skill (more on this probability estimate in [Half-Life Regression: A New Approach]()). At four bars, the skill is "golden" and considered fresh in the student's memory. At fewer bars, the skill has grown stale and may need practice. A student can tap the skill icon to access practice sessions and target her weakest words. For example, Figure 1(b) shows some weak words from the _Gerund_ skill. Practice sessions are identical to lessons, except that the exercises are taken from those indexed with words (lexeme tags) due for practice according to student model. As time passes, strength meters continuously update and decay until the student practices.

# Spaced Repetition Models

In this section, we describe several spaced repetition algorithms that might be incorporated into our student model. We begin with two common, established methods in language learning technology, and then present our half-life regression model which is a generalization of them.

## The Pimsleur Method

Pimsleur (1967) was perhaps the first to make mainstream practical use of the spacing and lag effects, with his audio-based language learning program (now a franchise by Simon & Schuster). He referred to his method as _graduated-interval recall_, whereby new vocabulary is introduced and then tested at exponentially increasing intervals, mixed with the introduction or review of other vocabulary. However, this approach is limited since the schedule is pre-recorded and cannot adapt to the learner's actual ability. Consider and English-speaking French student who easily learns a cognate like _pantalon_ (pants), but struggles to remember _manteau_ (coat). With the Primsleur method, she is forced to practice both words at the same fixed, increasing schedule.

## The Leitner System

Leitner (1972) proposed a different spaced repetition algorithm intended for use with flashcards. It is more adaptive than Pimsleur's, since the spacing intervals can increase or decrease depending on student performance. Figure 3 illustrates a popular variant of this method.

The main idea is to have a few boxes that correspond to different practice intervals: 1-day, 2-day, 4-day, and so on. All cards start out in the 1-day box, and if the student can remember and item after one day, it gets "promoted" to the 2-day box. Two days later, if she remembers it again, it gets promoted to the 4-day box, etc. Conversely, if she is incorrect, the card gets "demoted" to a shorter interval box. Using this approach, the hypothetical French student from [The Pimsleur Method]() would quickly promote _pantalon_ to a less frequent practice schedule, but continue reviewing _manteau_ often until she can regularly remember it.

Several electronic flashcard programs use the Leitner system to schedule practice, by organizing items into "virtual" boxes. In fact, when it first launched, Duolingo used a variant similar to Figure 3 to manage skill meter decay and practice. The present research was motivated by the need for a more accurate model, in response to student complaints that the Leitner-based skill meters did not adequately reflect what they had learned.

## Half-Life Regression: A New Approach

We now describe half-life regression (HLR), starting from psychological theory and combining it with modern machine learning techniques.

Central to the theory of memory is the _Ebbinghaus model_, also known as the _forgetting curve_ (Ebbinghaus, 1885). This posits that memory decays exponentially over time:

![p=2^{- \Delta / h}](https://render.githubusercontent.com/render/math?math=p%3D2%5E%7B-%20%5CDelta%20%2F%20h%7D) (1)

In this equation, `p` denotes the probability of correctly recalling an item (e.g. a word), which is a function of ![\Delta](https://render.githubusercontent.com/render/math?math=%5CDelta), the _lag time_ since the item was last practiced, and `h`, the _half-life_ or measure of strength in the learner's long-term memory.

Figure 4(a) shows a forgetting curve (1) with half-life `h = 1`. Consider the following cases:

1. ![\Delta = 0](https://render.githubusercontent.com/render/math?math=%5CDelta%20%3D%200). The word was just recently practiced, so ![p = 2^0 = 1.0](https://render.githubusercontent.com/render/math?math=p%20%3D%202%5E0%20%3D%201.0), conforming to the idea that it is fresh in memory and should be recalled correctly regardless of half-life.

2. ![\Delta = h](https://render.githubusercontent.com/render/math?math=%5CDelta%20%3D%20h). The lag time is equal to the half-life, so ![p = 2^{-1} = 0.5](https://render.githubusercontent.com/render/math?math=p%20%3D%202%5E%7B-1%7D%20%3D%200.5), and the student is on the verge of being unable to remember.

3. ![\Delta \gg h](https://render.githubusercontent.com/render/math?math=%5CDelta%20%5Cgg%20h). The word has not been practiced for a long time relative to its half-life, so it has probably been forgotten, e.g. ![p \approx 0](https://render.githubusercontent.com/render/math?math=p%20%5Capprox%200).

Let `x` denote a feature vector that summarizes a student's previous exposure to a particular word, and let the parameter vector ![\theta](https://render.githubusercontent.com/render/math?math=%5Ctheta) contain weights that correspond to each feature variable in `x`. Under the assumption that half-life should increase exponentially with each repeated exposure (a common practice in spacing and lag effect research), we let ![\hat{h}_\theta](https://render.githubusercontent.com/render/math?math=%5Chat%7Bh%7D_%5Ctheta) denote the estimated half-life, given by:

![\hat{h}_\theta = 2^{\theta \cdot x}](https://render.githubusercontent.com/render/math?math=%5Chat%7Bh%7D_%5Ctheta%20%3D%202%5E%7B%5Ctheta%20%5Ccdot%20x%7D) (2)

In fact, the Pimsleur and Leitner algorithms can be interpreted as special cases of (2) using a few fixed, hand-picked weights. See the Appendix for the derivation of ![\theta](https://render.githubusercontent.com/render/math?math=%5Ctheta) for these two methods.

For our purposes, however, we want to fit ![\theta](https://render.githubusercontent.com/render/math?math=%5Ctheta) emprirically to learning trace data, and accommodate an arbitrarily large set of interesting features (we discuss these features more in [Feature Sets]()). Suppose we have a data set `D = [(p, delta, x)]` made up of student-word practice sessions. Each data instance consists of the observed recall rate ![p^4](https://render.githubusercontent.com/render/math?math=p%5E4) (why is not `p`?), lag time ![\Delta](https://render.githubusercontent.com/render/math?math=%5CDelta) since the word was last seen, and a feature vector `x` designed to help personalize the learning experience. Our goal is to find the best model weights ![\theta*](https://render.githubusercontent.com/render/math?math=%5Ctheta*) to minimize some loss function ![l](https://render.githubusercontent.com/render/math?math=l):

To illustrate, Figure 4(b) shows a student-word learning trace over the course of a month. Each ✖ indicates a data instance: the vertical position is the observed recall rate `p` for each practice session, and the horizontal distance between points is the lag time ![\Delta](https://render.githubusercontent.com/render/math?math=%5CDelta) between sessions. Combining (1) and (2), the model prediction ![\hat{p}_\theta = 2^{-\Delta/\hat{h}_\theta}](https://render.githubusercontent.com/render/math?math=%5Chat%7Bp%7D_%5Ctheta%20%3D%202%5E%7B-%5CDelta%2F%5Chat%7Bh%7D_%5Ctheta%7D) is plotted as a dashed line over time (which resets to 1.0) after each exposure, since ![\Delta = 0](https://render.githubusercontent.com/render/math?math=%5CDelta%20%3D%200). The training loss function (3) aims to fit the predicted forgetting curves to observed data points for millions of student-word learning traces like this one.

We chose the ![L_2](https://render.githubusercontent.com/render/math?math=L_2)-regularized squared loss function, which in its basic form is given by:

where ✖ = `(p, delta, x)` is shorthand for the training data instance, and ![\lambda](https://render.githubusercontent.com/render/math?math=%5Clambda) is a parameter to control the regularization term and help prevent overfitting.

In practice, we found it useful to optimize for the half-life `h` in addition to the observed recall rate `p`. Since we do not know the "true" half-life of a given word in the student's memory - this is a hypothetical construct - we approximate it algebraically from (1) using `p` and ![\Delta](https://render.githubusercontent.com/render/math?math=%5CDelta). We solve for ![h = \dfrac{-\Delta}{\log_2 (p)}](https://render.githubusercontent.com/render/math?math=h%20%3D%20%5Cdfrac%7B-%5CDelta%7D%7B%5Clog_2%20(p)%7D) and use the final loss function:

where ![\alpha](https://render.githubusercontent.com/render/math?math=%5Calpha) is a parameter to control the relative importance of the half-life term in the overall training objective function. Since ![\l](https://render.githubusercontent.com/render/math?math=%5Cl) is smooth with respect to ![\theta](https://render.githubusercontent.com/render/math?math=%5Ctheta), we can fit the weights to student-word learning traces using gradient descent. See the Appendix for more details on our training and optimization procedures.