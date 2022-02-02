import deco
from deco.sources import Dataset
from tokenizers import Tokenizer
from transformers import TFElectraForMaskedLM, ElectraConfig, create_optimizer, TFElectraForPreTraining
import tensorflow as tf
import sys, glob, random
import tensorflow_addons as tfa

tokenizer = Tokenizer.from_file("tokenizer.json")
def tokenize(text):
    return tokenizer.encode(text).tokens

def encode(input):
    ids = []
    for token in input:
        id = tokenizer.token_to_id(token)
        ids.append(id)
    return ids

def shape_list(x: tf.Tensor):
    static = x.shape.as_list()
    dynamic = tf.shape(x)
    return [dynamic[i] if s is None else s for i, s in enumerate(static)]

class MyLoss(tf.keras.losses.Loss):
  def call(self, labels, logits):
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True, reduction=tf.keras.losses.Reduction.NONE)
    # make sure only labels that are not equal to -100
    # are taken into account as loss
    active_loss = tf.not_equal(tf.reshape(labels, (-1,)), -100)
    reduced_logits = tf.boolean_mask(tf.reshape(logits, (-1, shape_list(logits)[2])), active_loss)
    labels = tf.boolean_mask(tf.reshape(labels, (-1,)), active_loss)
    return loss_fn(labels, reduced_logits)

from keras_bert import AdamWarmup
strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    config = ElectraConfig(vocab_size=len(tokenizer.get_vocab()))
    gen_model = TFElectraForMaskedLM(config)
    gen_optimizer, _ = create_optimizer(5e-5, 100000, 10000)
    gen_model.compile(loss=MyLoss(), optimizer=gen_optimizer)

    disc_model = TFElectraForPreTraining(config)
    disc_optimizer, disc_schedule = create_optimizer(5e-5, 100000, 10000, adam_epsilon=1e-6)
    #disc_optimizer = tf.optimizers.Adam(learning_rate=disc_schedule, amsgrad=True, epsilon=0.1)
    print(disc_optimizer)
    disc_model.compile(optimizer=disc_optimizer, loss="binary_crossentropy")


files = sorted(glob.glob("abstracts/*.tsv"))
text = Dataset.from_lines(files).split_by("\n").map(tokenize, axis=1) \
    .concat(max_len=126).batch(64).cache()
mask = text.whole_word_mask(axis=1)
encoded = text.map(encode, axis=1)
masked = encoded.where(~mask, 4, axis=1) \
    .pad((2,3), axis=1).pad(0, length=128, axis=1)

gen_target = encoded.where(mask, -100).pad((-100, -100), axis=1).pad(-100, length=128, axis=1)
gen_loss = masked.zip(gen_target).train(gen_model)

unmasked = encoded.pad((2,3), axis=1).pad(0, length=128, axis=1)
output = masked.predict(gen_model).softmax().argmax(axis=2)
cleaned = output.where(masked==4, masked)
disc_target = cleaned==unmasked
disc_loss = unmasked.zip(disc_target).train(disc_model)

for item in gen_loss.zip(disc_loss).tb_log():
    print(item)

#tensorboard --logdir=/data/pubmed/log --port=4000 --bind_all --path_prefix=/test