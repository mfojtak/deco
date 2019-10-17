from deco.sources import Dataset
import numpy as np

class Fetch(Dataset):
    def __init__(self, parent):
        self.parent = parent
    def __iter__(self):
        data = []
        for item in self.parent:
            data.append(item)
        yield data

def fetch(self):
    return Fetch(self)

Dataset.fetch = fetch