from deco.sources import Dataset
import numpy as np

class Numpy(Dataset):
    def __init__(self, x: Dataset):
        pass
    def __iter__(self):
        for item in self.inputs():
            yield np.array(item)
            

def numpy(self):
    return Numpy(x=self)

Dataset.numpy = numpy