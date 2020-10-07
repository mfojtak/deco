from deco.sources import Dataset, Map
import random
from enum import Enum

def process_sentencepiece(x, rate, mask):
    res = []
    capturing = False
    for item in x:
        if item.startswith("▁"):
            if random.random() < rate:
                res.append(mask)
                capturing = True
            else:
                res.append(item)
                capturing = False
        else:
            if capturing:
                res.append(mask)
            else:
                res.append(item)
    return res

def process_wordpiece(x, rate, mask):
    res = []
    masked = []
    capturing = False
    for item in x:
        if not item.startswith("##"):
            if random.random() < rate:
                res.append(mask)
                masked.append(item)
                capturing = True
            else:
                res.append(item)
                masked.append("[PAD]")
                capturing = False
        else:
            if capturing:
                res.append(mask)
                masked.append(item)
            else:
                res.append(item)
                masked.append("[PAD]")
    return res, masked

class Mode(Enum):
    SENTENCEPIECE = "sentencepiece"
    WORDPIECE = "wordpiece"

def whole_word_mask(self, axis=0, rate=0.15, mask = "[MASK]", mode = Mode.WORDPIECE):
    if mode is Mode.SENTENCEPIECE:
        return Map(self, func=lambda x: process_sentencepiece(x, rate, mask), axis=axis)
    elif mode is Mode.WORDPIECE:
        return Map(self, func=lambda x: process_wordpiece(x, rate, mask), axis=axis)

Dataset.whole_word_mask = whole_word_mask