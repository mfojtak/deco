from deco.sources import Dataset
import numpy as np

class Lookup(Dataset):
    def __init__(self, parent, data, axis=0):
        self.parent = parent
        self.data = data
        self.axis = axis
    def __iter__(self):
        for item in self.parent:
            res = np.take(self.data, indices=item, axis=self.axis)
            yield res

def lookup(self, data, axis=0):
    return Lookup(self, data=data, axis=axis)

Dataset.lookup = lookup