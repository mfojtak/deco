from deco.sources import Dataset
import tensorflow as tf

class Argmax(Dataset):
    def __init__(self, input: Dataset, axis=None):
        self.axis = axis
    def __iter__(self):
        for item in self.inputs():
            res = tf.math.argmax(item, axis=self.axis)
            yield res

def argmax(self, axis=None):
    return Argmax(input=self, axis=axis)

Dataset.argmax = argmax