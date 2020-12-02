from nltk import FreqDist


def term_ratio(tf1: FreqDist,
               tf2: FreqDist,
               c=None,
               normalize=False):
    if normalize:
        if c is None:
            c = 1e-4
        return {word: (tf1[word] / tf1.N()) / (tf2[word] / tf2.N() + c)
                for word in tf1.keys()}
    else:
        if c is None:
            c = 1
        return {word: tf1[word] / (tf2[word] + c)
                for word in tf1.keys()}
