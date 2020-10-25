from deco.sources import Dataset
import asyncio

class Zip(Dataset):
    def __init__(self, *datasets: Dataset):
        pass
    def __iter__(self):
        yield from self.inputs()

def zip(*datasets: Dataset):
    return Zip(*datasets)

def zip_inst(self, *datasets: Dataset):
    return Zip(self, *datasets)

Dataset.zip = zip_inst