import sys
import deco
from deco.sources import Dataset
from tokenizers import Tokenizer
from transformers import TFElectraForMaskedLM, ElectraConfig, create_optimizer, \
                        TFElectraForPreTraining
import tensorflow as tf
import sys, glob, random
import numpy as np
import copy

#c = tf.ragged.constant([[True, False], [True]])
#x = tf.ragged.constant([[1, 2], [3]])
#res = tf.where(c, x=x, y=-100)
#print(res)
#sys.exit()

tokenizer = Tokenizer.from_file("tokenizer.json")
def tokenize(text):
    return tokenizer.encode(text).tokens

def encode(input):
    ids = []
    for token in input:
        id = tokenizer.token_to_id(token)
        ids.append(id)
    return ids

generator = TFElectraForMaskedLM.from_pretrained("output/generator_pretrained/")

config = ElectraConfig(vocab_size=len(tokenizer.get_vocab()))
model = TFElectraForPreTraining(config)
optimizer, schedule = create_optimizer(1e-4, 1000, 100)
model.compile(optimizer=optimizer, loss="binary_crossentropy")


files = glob.glob("abstracts/*.tsv")
#random.shuffle(files)
text = Dataset.from_lines(files).split_by("\n").map(tokenize, axis=1) \
    .concat(max_len=126).batch(64)
mask = text.whole_word_mask(axis=1)
encoded = text.map(encode, axis=1)
masked = encoded.where(~mask, 4, axis=1) \
    .pad((2,3), axis=1).pad(0, length=128, axis=1)
unmasked = encoded.pad((2,3), axis=1).pad(0, length=128, axis=1)
output = masked.predict(generator).softmax().argmax(axis=2)
cleaned = output.where(masked==4, masked)
target = cleaned==unmasked
loss = unmasked.zip(target).cache().train(model)

def walk(node):
    print(node)
    if len(node._inputs) == 0:
        print("Input:", node)
    if len(node._outputs) == 0:
        print("Output:", node)
    for child in node._inputs:
        walk(child)
walk(loss)
cp = copy.deepcopy(loss)
walk(cp)
sys.exit()

for item in loss.tb_log():
    print(item)



def gen():
    for item in unmasked.zip(target).cache():
        print(item[0])
        yield {"input_ids": item[0], "labels": item[1]}
model.fit(gen(), epochs=100, steps_per_epoch=1000, 
        callbacks=[tf.keras.callbacks.TensorBoard(log_dir="log/discriminator"),
                    tf.keras.callbacks.experimental.BackupAndRestore(backup_dir="tmp/disriminator")])