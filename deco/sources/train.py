from deco.sources import Dataset, Map
import numpy as np
from tensorflow.keras import Model
from tensorflow.keras.optimizers.schedules import LearningRateSchedule
import time

class Train(Dataset):
    def __init__(self, model: Model, x: Dataset, y: Dataset=None, save_path="log/{name}/model", save_freq=1000):
        self.model = model
        self.is_y = True if y else False
        self.save_path = save_path
        self.save_freq = save_freq
    def _format_output(self, data):
        lr = self.model.optimizer.learning_rate
        #if hasattr(self.model.optimizer, '_decayed_lr'):
        #    lr = self.model.optimizer._decayed_lr
        if isinstance(lr, LearningRateSchedule):
            lr = lr(self.model.optimizer.iterations)
        data["lr"] = lr.numpy()
        return data
    def _process(self, x, y, step):
        res = self.model.train_on_batch(x, y, return_dict=True)
        t = time.strftime("%Y%m%d-%H%M%S")
        sp = self.save_path.format(time=t, name=self.model.name, step=step)
        if step > 0 and step%self.save_freq == 0:
            self.model.save_weights(sp)
            print("Saving checkpoint to {}".format(sp))
        return self._format_output(res)

    def __iter__(self):
        
        if self.is_y:
            for step, x, y in enumerate(self.inputs()):
                yield self._process(x, y, step)
        else:
            for step, x in enumerate(self.inputs()):
                yield self._process(x[0], x[1], step)

def train(model, x: Dataset, y: Dataset=None):
    return Train(model, x, y)

def train_inst(self, model, save_path="log/{name}/model", save_freq=1000):
    return Train(model=model, x=self, save_path=save_path, save_freq=save_freq)

Dataset.train = train_inst