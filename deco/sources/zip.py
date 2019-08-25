from deco.sources import Dataset
import asyncio

class Zip(Dataset):
    def __init__(self, datasets):
        self.datasets = datasets
    async def __aiter__(self):
        iters = [dataset.__aiter__()
                    for dataset in self.datasets]
        
        while True:
            try:
                coros = [it.__anext__() for it in iters]
                items = await asyncio.gather(*coros)
            except StopAsyncIteration:
                break
            else:
                yield items

def zip(self, *datasets):
    return Zip([self] + list(datasets))
def __add__(self, other):
    return self.zip(other)

Dataset.zip = zip
Dataset.__add__ = __add__