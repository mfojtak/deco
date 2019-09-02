from deco.sources import Dataset
import numpy as np

class Batch(Dataset):
    def __init__(self, parent, batch_size):
        self.parent = parent
        self.batch_size = batch_size
    async def __aiter__(self):
        batch = []
        async for item in self.parent:
            batch.append(item)
            if len(batch) == self.batch_size:
                yield np.array(batch)
                batch = []
        if batch:
            yield np.array(batch)

def batch(self, batch_size):
    return Batch(self, batch_size)

Dataset.batch = batch