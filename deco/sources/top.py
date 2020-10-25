from deco.sources import Dataset

class Top(Dataset):
    def __init__(self, parent, top=10):
        self.top = top

    def __iter__(self):
        for i, item in enumerate(self.inputs()):
            if i<self.top:
                yield item
            else:
                break

def top(self, top):
    return Top(self, top)

Dataset.top = top