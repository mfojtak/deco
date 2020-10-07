from deco.sources import Dataset

class SplitBy(Dataset):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value
    def __iter__(self):
        agg = []
        for item in self.parent:
            if item == self.value:
                yield agg
                agg = []
            else:
                agg.append(item)
        if len(agg) > 0:
            yield agg

def split_by(self, value):
    return SplitBy(self, value)

Dataset.split_by = split_by