from deco.sources import Dataset, Map
import numpy as np
import tensorflow as tf           

class LogicalNot(Dataset):
    def __init__(self, x: Dataset):
        pass
    def __iter__(self):
        for item in self.inputs():
            x = item
            if isinstance(item, list):
                x = tf.ragged.constant(item)
            yield tf.logical_not(x)

def logical_not(self):
    return LogicalNot(x=self)

Dataset.logical_not = logical_not
Dataset.__invert__ = logical_not