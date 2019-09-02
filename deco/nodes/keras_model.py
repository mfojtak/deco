import os
os.environ['TF_KERAS'] = '1'
import tensorflow as tf
import numpy as np
import threading

class KerasModel:
    def __init__(self, path, custom_objects=None):
        self.path = path
        self.custom_objects = custom_objects
        self.model = None
        self.lock = threading.Lock()
    def _load(self):
        self.model = tf.keras.models.load_model(self.path, custom_objects=self.custom_objects)
        self.model._make_predict_function()
    def __call__(self, input):
        with self.lock:
            if not self.model:
                self._load()
        res = self.model.predict(np.array(input))
        return res