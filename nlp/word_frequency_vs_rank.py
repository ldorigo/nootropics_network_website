from nltk import FreqDist
import numpy as np


def word_frequency_vs_rank(text,
                           as_probability=False):
    frequency_distribution = FreqDist(text)
    frequency = np.asarray(sorted(frequency_distribution.values(),
                                  reverse=True))
    if as_probability:
        frequency / len(text)

    rank = np.arange(1, len(frequency) + 1)

    return rank, frequency
