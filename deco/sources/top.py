from deco.sources import Dataset

class Top(Dataset):
    def __init__(self, parent, top=10):
        self.parent = parent
        self.top = top

    def __iter__(self):
        iterator = iter(self.parent)
        for i in range(0,self.top):
            item = next(iterator)
            yield item

def top(self, top):
    return Top(self, top)

Dataset.top = top