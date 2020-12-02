from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def remove_stopwords(words: list,
                     language='english',
                     stem=False,
                     exclude=tuple()):

    # Load stopwords.
    if language == 'english':
        stop_words = stopwords.words('english')
    else:
        raise Exception('Invalid language: "' + '".')

    # Remove the stopwords on the list of excluded stopwords.
    stop_words = [stop_word for stop_word in stop_words
                  if stop_word not in exclude]

    # Stem if chosen by the user.
    if stem:
        stemmer = PorterStemmer()
        stop_words = [stemmer.stem(stop_word) for stop_word in stop_words]
        words = [stemmer.stem(word) for word in words]

    return [word for word in words
            if word.lower() not in stop_words]
