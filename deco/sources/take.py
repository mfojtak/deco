from deco.sources import Dataset
import numpy as np

class Take(Dataset):
    def __init__(self, parent, indices, axis=0):
        self.parent = parent
        self.indices = indices
        self.axis = axis
    def __iter__(self):
        for item in self.parent:
            res = np.take(item, indices=self.indices, axis=self.axis)
            yield res

def take(self, indices, axis=0):
    return Take(self, indices=indices, axis=axis)

Dataset.take = take