from deco.sources import Dataset
import numpy as np

def chunks(l, length, shift):
    for i in range(0, len(l), shift):
        yield l[i:i + length]


class Window(Dataset):
    def __init__(self, parent, size, step=None, axis=0):
        self.parent = parent
        self.size = size
        self.step = step
        if step == 0:
            self.step = size
        self.axis = axis
    async def __aiter__(self):
        if self.axis == 0:
            window = []
            async for item in self.parent:
                window.append(item)
                if len(window) == self.size:
                    yield window
                    window = []
            if window:
                yield window
        if self.axis == 1:
            async for item in self.parent:
                for chunk in chunks(item, self.size, self.step):
                    yield chunk

def batch(self, batch_size):
    return Window(self, batch_size)

def window(self, size, step=None, axis=0):
    return Window(self, size, step, axis)

Dataset.batch = batch
Dataset.window = window