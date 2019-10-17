from abc import ABC, abstractmethod

class Sink(ABC):
    @abstractmethod
    def __iter__(self):
        pass
    def eval(self):
        it = iter(self)
        while True:
            try:
                next(it)
            except StopIteration:
                break