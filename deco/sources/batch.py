from deco.sources import Dataset

class Batch(Dataset):
    def __init__(self, parent, batch_size):
        self.parent = parent
        self.batch_size = batch_size
    async def __aiter__(self):
        batch = []
        async for item in self.parent:
            batch.append(item)
            if len(batch) == self.batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

def batch(self, batch_size):
    return Batch(self, batch_size)

Dataset.batch = batch