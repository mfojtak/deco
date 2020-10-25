from deco.sources import Dataset
import numpy as np

class Equal(Dataset):
    def __init__(self, x1, x2):
        self.x2 = None
        if not isinstance(x2, Dataset):
            self.x2 = x2
    def __iter__(self):
        if self.x2 != None:
            for x1 in self.inputs():
                yield np.equal(x1, self.x2)
        else:
            for x1, x2 in self.inputs():
                yield np.equal(x1, x2)

def equal(self, x2):
    return Equal(self, x2)

Dataset.equal = equal
Dataset.__eq__ = equal