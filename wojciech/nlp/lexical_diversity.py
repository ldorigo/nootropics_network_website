import nltk


def lexical_diversity(text: nltk.Text):
    return len(set(text)) / len(text)
