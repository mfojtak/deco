from abc import ABC, abstractmethod

class Dataset(ABC):
    @abstractmethod
    async def __aiter__(self):
        pass