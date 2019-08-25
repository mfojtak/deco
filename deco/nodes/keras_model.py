from deco.nodes import Transform
import os
os.environ['TF_KERAS'] = '1'
import tensorflow as tf

class KerasModel(Transform):
    def __init__(self, name, path, custom_objects=None):
        super().__init__(name)
        self.path = path
        self.custom_objects = custom_objects
    def _load(self):
        self.model = tf.keras.models.load_model(self.path, custom_objects=self.custom_objects)
    def _unload(self):
        del self.model
    async def _eval(self, input):
        res = self.model.predict(input)
        return res
    async def _info(self):
        return self.model.get_config()