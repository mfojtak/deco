from deco.sources import Dataset

class IterableDataset(Dataset):
    def __init__(self, parent):
        self.parent = parent
    def __iter__(self):
        for item in self.parent:
            yield item
    def get_data(self):
        return self.parent
    def set_data(self, data):
        self.parent = data

def from_iterable(parent):
    return IterableDataset(parent=parent)

Dataset.create = from_iterable