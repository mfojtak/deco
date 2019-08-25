from deco.sources import Dataset

class IterableDataset(Dataset):
    def __init__(self, parent):
        self.parent = parent
    async def __aiter__(self):
        for item in self.parent:
            yield item

def from_iterable(parent):
    return IterableDataset(parent)

Dataset.from_iterable = from_iterable