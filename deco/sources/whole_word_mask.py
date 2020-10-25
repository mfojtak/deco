from deco.sources import Dataset, Map
import random
from enum import Enum

def process_sentencepiece(x, rate):
    res = []
    capturing = False
    for item in x:
        if item.startswith("▁"):
            if random.random() < rate:
                res.append(1)
                capturing = True
            else:
                res.append(0)
                capturing = False
        else:
            if capturing:
                res.append(1)
            else:
                res.append(0)
    return res

def process_wordpiece(x, rate):
    res = []
    capturing = False
    for item in x:
        if not item.startswith("##"):
            if random.random() < rate:
                res.append(True)
                capturing = True
            else:
                res.append(False)
                capturing = False
        else:
            if capturing:
                res.append(True)
            else:
                res.append(False)
    return res

class Mode(Enum):
    SENTENCEPIECE = "sentencepiece"
    WORDPIECE = "wordpiece"

def whole_word_mask(self, axis=0, rate=0.15, mode = Mode.WORDPIECE):
    if mode is Mode.SENTENCEPIECE:
        return Map(self, func=lambda x: process_sentencepiece(x, rate), axis=axis)
    elif mode is Mode.WORDPIECE:
        return Map(self, func=lambda x: process_wordpiece(x, rate), axis=axis)

Dataset.whole_word_mask = whole_word_mask