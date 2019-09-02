from deco.sources import Dataset, Batch
import deco
import asyncio
import multiprocessing
from concurrent.futures import Executor
from typing import Callable
import numpy as np

class Map(Dataset):
    def __init__(self, parent: Dataset, func: Callable, axis=0,
                    executor: Executor=None, parallel_tasks: int=None):
        self.parent = parent
        self.func = func
        self.axis = axis
        self.executor = executor
        self.parallel_tasks = parallel_tasks
        if not self.parallel_tasks:
            self.parallel_tasks = multiprocessing.cpu_count()
        if not self.executor:
            self.executor = deco.default_executor
    async def __aiter__(self):
        if self.axis == 1:
            self.func = np.vectorize(self.func)
        loop = asyncio.get_running_loop()
        async for batch in self.parent.batch(self.parallel_tasks):
            coros = []
            for item in batch:
                coros.append(loop.run_in_executor(self.executor, self.func, item))
            items = await asyncio.gather(*coros)
            for item in items:
                yield item


def map(self, func, axis=0):
    return Map(self, func=func, axis=axis)

Dataset.map = map