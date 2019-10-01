from deco.sources import Dataset
import numpy as np


def squeeze_rec(item):
    if isinstance(item, list):
        new_list = []
        for subitem in item:
            new_list.append(squeeze_rec(subitem))
        if len(new_list) == 1:
            new_list = new_list[0]
        return new_list
    else:
        return item

class Squeeze(Dataset):
    def __init__(self, parent):
        self.parent = parent
    async def __iter__(self):
        for item in self.parent:
            yield squeeze_rec(item)
            #yield np.squeeze(item)


def squeeze(self):
    return Squeeze(self)

Dataset.squeeze = squeeze