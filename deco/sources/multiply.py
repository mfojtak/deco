from deco.sources import Dataset

class Multiply(Dataset):
    def __init__(self, x1: Dataset, x2):
        self.x2 = None
        if not isinstance(x2, Dataset):
            self.x2 = x2
    def __iter__(self):
        if self.x2 != None:
            for x1 in self.inputs():
                yield x1 * self.x2
        else:
            for x1, x2 in self.inputs():
                yield x1 * x2

def multiply(x1: Dataset, x2):
    return Multiply(x1, x2)

def multiply_inst(self, x2):
    return Multiply(x1=self, x2=x2)

Dataset.multiply = multiply_inst
Dataset.__mul__ = multiply_inst