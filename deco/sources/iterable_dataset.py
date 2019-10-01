from deco.sources import Dataset

class IterableDataset(Dataset):
    def __init__(self, parent, axis=1):
        self.parent = parent
    def __iter__(self):
        for item in self.parent:
            yield item

def from_iterable(parent):
    return IterableDataset(parent)

Dataset.from_iterable = from_iterable