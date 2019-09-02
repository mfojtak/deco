from deco.sources import Dataset
import numpy as np

class Take(Dataset):
    def __init__(self, parent, indices, axis=1):
        self.parent = parent
        self.indices = indices
        self.axis = axis
    async def __aiter__(self):
        if self.axis == 0:
            data = []
            async for item in self.parent:
                data.append(item)
            res = np.take(data, self.indices, self.axis)
            yield res
        else:
            async for item in self.parent:
                res = np.take(item, indices=self.indices, axis=self.axis-1)
                yield res

def take(self, indices, axis=1):
    return Take(self, indices=indices, axis=axis)

Dataset.take = take