from deco.sources import Dataset
import numpy as np

class Concat(Dataset):
    def __init__(self, parent, axis=1):
        self.parent = parent
        self.axis = axis
    def __iter__(self):
        if self.axis == 0:
            flattened = []
            for item in self.parent:
                for y in item:
                    flattened.append(y)
            yield flattened
        if self.axis == 1:
            for item in self.parent:
                flattened = [y for x in item for y in x]
                yield flattened

def concat(self, axis=1):
    return Concat(self, axis=axis)

Dataset.concat = concat