import nltk.data
nltk.download('punkt')
from collections import Iterable
from deco.sources import Dataset
from deco.sources import Map
import sys

class SentenceSplitter:
    def __init__(self):
        self.tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    def __call__(self, input):
        res = self.tokenizer.tokenize(input)
        return res

def split_sentence(self, axis=0):
    splitter = SentenceSplitter()
    return Map(self, splitter, axis=axis)

Dataset.split_sentence = split_sentence
