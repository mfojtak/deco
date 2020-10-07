from deco.sources import Dataset, Map
from functools import partial
import numpy as np

def transpose(self, axis=0, axes=(1,0,2)):
    func = partial(np.transpose, axes=axes)
    return Map(self, func=func, axis=axis)

Dataset.transpose = transpose