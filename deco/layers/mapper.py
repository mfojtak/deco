import tensorflow as tf
import sys


class Mapper(tf.keras.layers.Layer):

    def __init__(self, map, sort='DESCENDING', batch_dims=0):
        super(Mapper, self).__init__()
        self.map = map
        self.map_tensor = tf.constant(map)
        self.sort = sort
        self.batch_dims = batch_dims

    def call(self, input):
        indexes = self.map
        values = input
        if self.sort is not None:
            sorted_i = tf.argsort(input, direction=self.sort)
            values = tf.gather(input, sorted_i, batch_dims=self.batch_dims)
            indexes = tf.gather(self.map, sorted_i)
        return indexes, values

    def get_config(self):
        return {'map': self.map, 'sort': self.sort, 'batch_dims': self.batch_dims}

#import collections
#t = tf.constant([[1,2,3], [3,2,1], [1,4,2]])
#print(isinstance((1,2), collections.Sequence))
#mapper = Mapper([1234, 5678, 901234], batch_dims=1)
#res = mapper(t)
#print(res) 
