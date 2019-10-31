from deco.sources import Dataset, Map
import random

def process(x, rate, mask):
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


def whole_word_mask(self, axis=0, rate=0.3, mask = "[MASK]"):
    return Map(self, func=lambda x: process(x, rate, mask), axis=axis)

Dataset.whole_word_mask = whole_word_mask