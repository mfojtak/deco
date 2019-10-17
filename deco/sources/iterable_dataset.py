from deco.sources import Dataset

class IterableDataset(Dataset):
    def __init__(self, parent):
        self.parent = parent
    def __iter__(self):
        for item in self.parent:
            yield item

def from_iterable(parent):
    return IterableDataset(parent)

Dataset.create = from_iterable