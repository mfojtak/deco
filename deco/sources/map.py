from deco.sources import Dataset, Window
from deco.utils import default_executor
import asyncio
import multiprocessing
from concurrent.futures import Executor
from typing import Callable
import numpy as np
import sys
from enum import Enum

class Output(Enum):
    NUMPY = "numpy"
    LIST = "list"
    TFRAGGED = "tfragged"

def vectorize( fn, output):
    def do_it (array):
        res = [fn(p) for p in array]
        if output == Output.NUMPY:
            res = np.array(res)
        return res
    return do_it

class Map(Dataset):
    def __init__(self, parent: Dataset, func: Callable, axis=0, output=Output.LIST):
        #self.parent = parent
        self.func = func
        self.axis = axis
        #self.executor = executor
        #self.parallel_tasks = parallel_tasks
        self.output = output
        #self.chunksize = 100
        #if not self.parallel_tasks:
        #    self.parallel_tasks = multiprocessing.cpu_count() * 2
        #if not self.executor:
        #    self.executor = default_executor
    def __iter__(self):
        if self.axis == 1:
            self.func = vectorize(self.func, self.output)
        if self.axis == 2:
            self.func = vectorize(vectorize(self.func, self.output), self.output)
        for item in self.inputs():
            yield self.func(item)
        #for batch in self.parent.batch(self.parallel_tasks * self.chunksize):
        #    result = self.executor.map(self.func, batch, chunksize=self.chunksize)
        #    for item in result:
        #        yield item


def map(self, func, axis=0, output=Output.LIST):
    return Map(self, func=func, axis=axis, output=output)

Dataset.map = map