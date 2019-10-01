from deco.sources import Dataset

class Constant(Dataset):
    def __init__(self, parent):
        self.parent = parent
    def __iter__(self):
            yield self.parent

def constant(parent):
    return Constant(parent)

Dataset.constant = constant