from deco.sources import Dataset
import tensorflow as tf
from typing import Callable
import numpy as np

class Predict(Dataset):
    def __init__(self, x: Dataset, model: Callable, device=None):
        self.model = model
        self.device = device
    def __iter__(self):
        for item in self.inputs():
            x = np.array(item) if isinstance(item, list) else item
            if self.device == None:
                res = self.model(x, training=False)
            else:
                with tf.device("/CPU:0" if self.device == -1 else "/device:GPU:{}".format(self.device)):
                    res = self.model(x, training=False)
            yield res[0]

def predict(self, model: Callable, device=None):
    return Predict(x=self, model=model, device=device)

Dataset.predict = predict