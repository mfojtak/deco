from deco.sources import Dataset, Batch
import deco
import asyncio
import multiprocessing
from concurrent.futures import Executor
from typing import Callable

class Map(Dataset):
    def __init__(self, parent: Dataset, func: Callable, executor: Executor=None, parallel_tasks: int=None):
        self.parent = parent
        self.func = func
        self.executor = executor
        self.parallel_tasks = parallel_tasks
        if not self.parallel_tasks:
            self.parallel_tasks = multiprocessing.cpu_count()
        if not self.executor:
            self.executor = deco.default_executor
    async def __aiter__(self):
        loop = asyncio.get_running_loop()
        async for batch in self.parent.batch(self.parallel_tasks):
            coros = []
            for item in batch:
                coros.append(loop.run_in_executor(self.executor, self.func, item))
            items = await asyncio.gather(*coros)
            for item in items:
                yield item


def map(self, func):
    return Map(self, func)

Dataset.map = map