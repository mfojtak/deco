from deco.sources import Dataset, Map
from functools import partial
import numpy as np

def process(item, values, length, counts):
    if length:
        diff = length - len(item)
        res = np.pad(item, (0, diff), 'constant', constant_values=values)
    else:
        res = np.pad(item, counts, 'constant', constant_values=values)
    return res

def pad(self, values, length=None, counts=(1,1), axis=0):
    func = partial(process, values=values, length=length, counts=counts)
    return Map(self, func=func, axis=axis)

Dataset.pad = pad