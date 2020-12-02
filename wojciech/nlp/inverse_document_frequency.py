from nltk import FreqDist
import numpy as np
from typing import Any
# from tqdm import tqdm


def inverse_document_frequency(terms: Any,
                               documents: list,
                               type: str = 'regular',
                               term_document: list = None):

    return_dict = True

    # Terms will be regarded as a list.
    # If terms is set to none, set terms to all the terms in the term document
    if terms is None:
        terms = set(term_document)

    # If the terms is a string, the output of the function will also be
    # a string.
    elif isinstance(terms, str):
        return_dict = False
        terms = [terms]

    n_documents = len(documents)
    documents = [set(document) for document in documents]
    n_documents_containing =\
        {term: np.sum([term in document for document in documents])
         for term in terms}

    if type.lower() == 'regular':
        result = {
            term: np.log10(n_documents / n_documents_containing[term])
            for term in terms}

    elif type.lower() == 'smooth':
        result = {
            term: 1 + np.log10(n_documents / (1 + n_documents_containing[term]))
            for term in terms}

    elif type.lower() == 'max':
        n_documents_containing = dict()

        for word in term_document:
            for document in documents:
                if word in document:
                    n_documents_containing[word] += 1

        max_n = max(n_documents_containing.values())

        result = {term: np.log10(max_n / (1 + n_documents_containing[term]))
                  for term in terms}

    elif type.lower() == 'probabilistic':
        result = \
            {term: np.log10((n_documents - n_documents_containing[term])
                            / n_documents_containing[term])
             for term in terms}

    else:
        raise Exception('Unknown type: "' + type + '".')

    if not return_dict:
        result = result[terms[0]]

    return result
