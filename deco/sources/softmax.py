from deco.sources import Dataset
import tensorflow as tf

class Softmax(Dataset):
    def __init__(self, logits: Dataset, axis=None):
        self.axis = axis
    def __iter__(self):
        for item in self.inputs():
            res = tf.nn.softmax(item, axis=self.axis)
            yield res

def softmax(self, axis=None):
    return Softmax(logits=self, axis=axis)

Dataset.softmax = softmax