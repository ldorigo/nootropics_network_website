import nltk


def stress(pronunciation: nltk.Text):
    return [character
            for phoneme in pronunciation
            for character in phoneme
            if character.isdigit()]
