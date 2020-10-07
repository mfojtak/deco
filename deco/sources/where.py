from deco.sources import Dataset
import numpy as np

class Where(Dataset):
    def __init__(self, parent, cond):
        self.parent = parent
        self.cond = cond
    def __iter__(self):
        for item in self.parent:
            if self.cond(item):
                yield item

def where(self, cond):
    return Where(self, cond)

Dataset.where = where