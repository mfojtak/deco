from deco.sources import Dataset, Map
import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers.schedules import LearningRateSchedule

class Train(Dataset):
    def __init__(self, model: tf.keras.Model, x: Dataset, y: Dataset=None):
        self.model = model
        self.is_y = True if y else False
    def _format_output(self, data):
        lr = self.model.optimizer.learning_rate
        if isinstance(lr, LearningRateSchedule):
            lr = lr(self.model.optimizer.iterations)
        data["lr"] = lr.numpy()
        return data
    def __iter__(self):
        if self.is_y:
            for x, y in self.inputs():
                res = self.model.train_on_batch(x, y, return_dict=True)
                yield self._format_output(res)
        else:
            for x in self.inputs():
                res = self.model.train_on_batch(x[0], x[1], return_dict=True)
                yield self._format_output(res)

def train(model, x: Dataset, y: Dataset=None):
    return Train(model, x, y)

def train_inst(self, model):
    return Train(model=model, x=self)

Dataset.train = train_inst