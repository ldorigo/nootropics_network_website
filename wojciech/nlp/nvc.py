from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
from pathlib import Path


def nvc():
    corpus_root = str(Path(__file__).parent / 'Nonviolent_Communication')
    return PlaintextCorpusReader(corpus_root, '.*', RegexpTokenizer(r"[\w']+"))
