from nltk import FreqDist
import numpy as np
from typing import Any


def term_frequency(terms: Any,
                   document: list,
                   type: str = 'raw count',
                   K=0.5):
    return_dict = True

    if terms is None:
        terms = set(document)

    elif isinstance(terms, str):
        return_dict = False
        terms = [terms]

    if type.lower() == 'binary':
        document_set = set(document)
        result = {term: term in document_set
                  for term in terms}
    else:
        fd = FreqDist(document)
        n_terms = fd.N()

        if type.lower() == 'raw count':
            result = {term: fd[term] for term in fd}

        elif type.lower() == 'frequency':
            result = {term: fd[term] / n_terms for term in terms}

        elif type.lower() == 'log normalized':
            result = {term: np.log10(1 + fd[term]) for term in terms}

        elif type.lower() == 'double normalized K':
            count_max_term = np.max(fd.values())

            result = {term: K + (1 - K) * fd[term] / count_max_term
                      for term in terms}

        else:
            raise Exception('Unknown type: "' + type + '".')

        if not return_dict:
            result = result[terms[0]]

        return result
