from deco.sources import Dataset
import numpy as np

class FullLike(Dataset):
    def __init__(self, a, fill_value):
        self.fill_value = fill_value
    def __iter__(self):
        for item in self.inputs():
            yield np.full_like(item, self.fill_value)

def full_like(self, fill_value):
    return FullLike(self, fill_value)

Dataset.full_like = full_like