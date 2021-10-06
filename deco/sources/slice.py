from deco.sources import Dataset, Take
from copy import deepcopy

class Slice(Dataset):
    def __init__(self, x: Dataset, start, stop, step, axis=0):
        self._start = start
        self._stop = stop
        self._step = step
        self._axis = axis
        self._deepcopy_input = True
    @property
    def step(self):
        return self._step
    @step.setter
    def step(self, value):
        self._step=value
    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, value):
        self._start=value
    def __iter__(self):
        if self._start == None:
            self._start = 0
        if self._axis == 0:
            for i, item in enumerate(self.inputs()):
                if self._start != None and i < self._start:
                    continue
                if self._stop != None and i >= self._stop:
                    break
                if self._step != None and (i-self._start)%self._step != 0:
                    continue
                yield item
    def __deepcopy__(self, memo):
        inp = self._inputs[0]
        if self._deepcopy_input:
            inp = deepcopy(inp, memo)
        c = Slice(inp, self._start, self._stop, self._step, self._axis)
        c._deepcopy_input = self._deepcopy_input
        #memo[id(self)] = c
        return c
        

def slice_inst(self, start, stop, step, axis=0):
    return Slice(self, start, stop, step, axis)

Dataset.slice = slice_inst

def getitem(self, key):
    if isinstance(key, slice):
        return Slice(self, key.start, key.stop, key.step)
    return Take(self, indices=key)

Dataset.__getitem__ = getitem