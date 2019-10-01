from deco.sources import Dataset
import asyncio

class Zip(Dataset):
    def __init__(self, datasets):
        self.datasets = datasets
    def __iter__(self):
        iters = [iter(dataset)
                    for dataset in self.datasets]
        
        while True:
            try:
                items = [next(it) for it in iters]
            except StopIteration:
                break
            else:
                yield items

def zip(self, *datasets):
    return Zip([self] + list(datasets))
def __add__(self, other):
    return self.zip(other)

Dataset.zip = zip
Dataset.__add__ = __add__