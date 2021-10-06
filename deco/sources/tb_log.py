from deco.sources import Dataset, Map
import numpy as np
import tensorflow as tf
import time        

def handle(data, postfix, step):
    if isinstance(data, (list, tuple)):
        for i, item in enumerate(data):
            new_postfix = "{}_{}".format(postfix, i)
            handle(item, new_postfix, step)
    elif isinstance(data, dict):
        for key in data.keys():
            name = key + postfix
            tf.summary.scalar(name, data=data[key], step=step)
    else:
        name = "var" + postfix
        tf.summary.scalar(name, data=data, step=step)

class TbLog(Dataset):
    def __init__(self, data: Dataset, folder: str="log/{time}"):
        self.folder = folder
    
    def __iter__(self):
        t = time.strftime("%Y%m%d-%H%M%S")
        self.folder = self.folder.format(time=t)
        
        writer = tf.summary.create_file_writer(self.folder)
        with writer.as_default():
            for step, data in enumerate(self.inputs()):
                handle(data, "", step)
                if step%10 == 0:
                    writer.flush()
                yield data


def tb_log(self, folder="log/{time}"):
    return TbLog(self, folder)

Dataset.tb_log = tb_log