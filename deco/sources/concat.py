from deco.sources import Dataset
import numpy as np

def gen(parent, max_len):
    flattened = []
    for item in parent:
        item_truncated = item
        if len(item) > max_len:
            item_truncated = item[:max_len]
        if max_len > 0 and len(item_truncated) + len(flattened) > max_len:
            yield flattened
            flattened = []
        flattened += item_truncated
    yield flattened

class Concat(Dataset):
    def __init__(self, parent, axis=1, max_len=-1):
        self.parent = parent
        self.axis = axis
        self.max_len = max_len
    def __iter__(self):
        if self.axis == 0:
            for item in gen(self.parent, self.max_len):
                yield item
        if self.axis == 1:
            for paritem in self.parent:
                for item in gen(paritem, self.max_len):
                    yield item

def concat(self, axis=1, max_len=-1):
    return Concat(self, axis=axis, max_len=max_len)

Dataset.concat = concat