import numpy as np
from deco.sources import Dataset

class Expand(Dataset):
    def __init__(self, parent, axis=0):
        self.parent = parent
        self.axis = axis
    async def __aiter__(self):
        async for item in self.parent:
            res = np.expand_dims(item, self.axis)
            yield res

def expand(self, axis=0):
    return Expand(self, axis=axis)

Dataset.expand = expand