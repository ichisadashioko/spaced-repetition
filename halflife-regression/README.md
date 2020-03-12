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