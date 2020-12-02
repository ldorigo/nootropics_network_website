import nltk


def unusual_words(text: nltk.Text,
                  language='english'):
    text_vocab = set(w.lower() for w in text if w.isalpha())

    if language == 'english':
        usual_vocab = set(w.lower() for w in nltk.corpus.words.words())
    else:
        raise Exception('Invalid language: "' + language + '".')

    unusual_vocab = text_vocab - usual_vocab

    return sorted(unusual_vocab)
