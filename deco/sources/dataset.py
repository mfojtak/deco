from abc import ABC, abstractmethod

class Dataset(ABC):
    @abstractmethod
    def __iter__(self):
        pass