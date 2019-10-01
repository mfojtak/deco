from deco.sources import Dataset, Map
import random

def shuffled(x):
    return random.sample(x, len(x))

def shuffle(self, axis=0):
    return Map(self, func=shuffled, axis=axis)

Dataset.shuffle = shuffle
