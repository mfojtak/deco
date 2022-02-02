import deco
from deco.sources import Dataset
from tokenizers import Tokenizer
from transformers import TFElectraForMaskedLM, ElectraConfig, create_optimizer
import tensorflow as tf
import sys, glob, random

tokenizer = Tokenizer.from_file("tokenizer.json")
def tokenize(text):
    return tokenizer.encode(text).tokens

def encode(input):
    ids = []
    for token in input:
        id = tokenizer.token_to_id(token)
        ids.append(id)
    return ids

files = glob.glob("abstracts/*.tsv")
random.shuffle(files)
text = Dataset.from_lines(files).split_by("\n").map(tokenize, axis=1) \
    .concat(max_len=126)
mask = text.whole_word_mask()
encoded = text.map(encode)
masked = encoded.where(mask.logical_not(), 4).pad((2,3)).pad(0, length=128)
target = encoded.where(mask, -100).pad((-100, -100)).pad(-100, length=128)
ds = masked.zip(target).batch(64).transpose().cache()


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

config = ElectraConfig(vocab_size=len(tokenizer.get_vocab()))
model = TFElectraForMaskedLM(config)
optimizer, schedule = create_optimizer(1e-4, 100000, 10000)
model.compile(loss=MyLoss(), optimizer=optimizer)
data = next(iter(ds))
res = model(data[0])
model.load_weights("output/generator_model_100/model")
res = model(data[0])

def gen():
    for item in ds:
        yield item[0], item[1]

model.fit(gen(), epochs=100, steps_per_epoch=1000, 
        callbacks=[tf.keras.callbacks.TensorBoard(log_dir="log"),
                    tf.keras.callbacks.experimental.BackupAndRestore(backup_dir="tmp")])

model.save_pretrained("output/generator_pretrained")
#optimizer=create_optimizer(1e-4, 100000, 10000)

#tensorboard --logdir=/data/pubmed/log --port=4000 --bind_all --path_prefix=/test
