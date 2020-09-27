import tensorflow as tf
import sys


class Mapper(tf.keras.layers.Layer):

    def __init__(self, map, sort='DESCENDING'):
        super(Mapper, self).__init__()
        self.map = map
        self.map_tensor = tf.constant(map)
        self.sort = sort

    def call(self, input):
        indexes = self.map
        values = input
        if self.sort is not None:
            sorted_i = tf.argsort(input, direction=self.sort)
            values = tf.gather(input, sorted_i)
            indexes = tf.gather(self.map, sorted_i)
        return indexes, values

    def get_config(self):
        return {'map': self.map, 'sort': self.sort}

#import collections
#t = tf.constant([1,2,3])
#print(isinstance((1,2), collections.Sequence))
#mapper = Mapper([1234, 5678, 901234])
#res = mapper([0.1, 0.9, 0.2])
#print(res) 
