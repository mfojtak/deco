#!/usr/bin/env python

import os
os.environ['TF_KERAS'] = '1'
import tensorflow as tf
#from tensorflow import keras
#import keras
from keras_bert import load_trained_model_from_checkpoint, bert
import sys

import argparse

parser = argparse.ArgumentParser(description='Exports keras model to serving format')
parser.add_argument('--input', action="store", dest="input")
parser.add_argument('--output', action="store", dest="output")

args = parser.parse_args()

model = tf.keras.models.load_model(args.input, custom_objects = bert.get_custom_objects())
tf.keras.experimental.export_saved_model(model, args.output, custom_objects = bert.get_custom_objects())

#python export_to_serving.py --input /data/develop/logs/class_keras5/model_1.h5 --output /data/develop/models/class/1
