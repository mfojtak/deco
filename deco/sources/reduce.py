from deco.sources import Map, Dataset, Window
import deco
import asyncio
import multiprocessing
from concurrent.futures import Executor
from typing import Callable
import numpy as np
import sys


class Reduce:
    def __init__(self, parent: Dataset, func: Callable,
                    executor: Executor=None):
        self.parent = parent
        self.func = func
        self.executor = executor
        if not self.executor:
            self.executor = deco.default_executor
    def __call__(self):
        agg = []
        for item in self.parent:
            agg.append(item)
        return self.func(agg)


def reduce(self, func):
    return Reduce(self, func=func)

Dataset.reduce = reduce