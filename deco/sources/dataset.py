from abc import ABC, abstractmethod

class Dataset(ABC):
    @abstractmethod
    def __iter__(self):
        pass
    def eval(self):
        res = []
        for item in self:
            res.append(item)
        if len(res) == 1:
            return res[0]
        return res 