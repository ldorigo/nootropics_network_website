import nltk


def content_fraction(text: nltk.Text,
                     language='english'):
    if language == 'english':
        stopwords = nltk.corpus.stopwords.words('english')
    else:
        raise Exception('Invalid language: "' + language + '".')

    content = [word for word in text if word.lower() not in stopwords]
    return len(content) / len(text)