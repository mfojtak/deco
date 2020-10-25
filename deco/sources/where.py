from deco.sources import Dataset
import numpy as np

class Where(Dataset):
    def __init__(self, cond: Dataset, x: Dataset, y, axis=0):
        self.y = None
        self.axis = axis
        if not isinstance(y, Dataset):
            self.y = y
    def __iter__(self):
        if self.y != None:
            if self.axis == 0:
                for cond, x in self.inputs():
                    yield np.where(cond, x, self.y)
            if self.axis == 1:
                for cond, x in self.inputs():
                    res = []
                    for subcond, subx in zip(cond, x):
                        res.append(np.where(subcond, subx, self.y))
                    yield res
        else:
            for cond, x, y in self.inputs():
                yield np.where(cond, x, y)
            

def where(self, cond, y, axis=0):
    return Where(cond=cond, x=self, y=y, axis=axis)

Dataset.where = where