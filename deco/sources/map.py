from deco.sources import Dataset, Window
import deco
import asyncio
import multiprocessing
from concurrent.futures import Executor
from typing import Callable
import numpy as np
import sys

def vectorize( fn):
    def do_it (array):
        return [fn(p) for p in array]
    return do_it

class Map(Dataset):
    def __init__(self, parent: Dataset, func: Callable, axis=0,
                    executor: Executor=None, parallel_tasks: int=None):
        self.parent = parent
        self.func = func
        self.axis = axis
        self.executor = executor
        self.parallel_tasks = parallel_tasks
        self.chunksize = 100
        if not self.parallel_tasks:
            self.parallel_tasks = multiprocessing.cpu_count() * 2
        if not self.executor:
            self.executor = deco.default_executor
    def __iter__(self):
        if self.axis == 1:
            self.func = vectorize(self.func)
        if self.axis == 2:
            self.func = vectorize(vectorize(self.func))
        for batch in self.parent.batch(self.parallel_tasks * self.chunksize):
            result = self.executor.map(self.func, batch, chunksize=self.chunksize)
            for item in result:
                yield item


def map(self, func, axis=0):
    return Map(self, func=func, axis=axis)

Dataset.map = map