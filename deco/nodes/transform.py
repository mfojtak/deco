from abc import ABC, abstractmethod
from enum import Enum

class Status(Enum):
    UNLOADED = 1
    IDLE = 2
    LOADING = 3
    EVALUATING = 4

class Transform(ABC):
    def __init__(self, name):
        self.name = name
        self.status = Status.UNLOADED
    @abstractmethod
    def _load(self):
        pass
    @abstractmethod
    def _unload(self):
        pass
    @abstractmethod
    async def _eval(self, input):
        pass
    @abstractmethod
    async def _info(self):
        pass
    async def eval(self, input):
        if self.status == Status.UNLOADED:
            self.load()
        self.status = Status.EVALUATING
        res = await self._eval(input)
        self.status = Status.IDLE
        return res
    async def __call__(self, input):
        res = await self.eval(input)
        return res
    def load(self):
        self.status = Status.LOADING
        self._load()
        self.status = Status.IDLE
    async def info(self):
        if self.status == Status.UNLOADED:
            self.load()
        info = await self._info()
        return info
    