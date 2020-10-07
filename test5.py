from transformers import ElectraConfig, ElectraTokenizerFast, TFElectraForMaskedLM, create_optimizer
from transformers import DataCollatorForLanguageModeling, TFTrainer, TFTrainingArguments, LineByLineTextDataset
#from tokenizers import Tokenizer
#from tokenizers.models import WordPiece
from transformers.modeling_tf_utils import TFMaskedLanguageModelingLoss
import deco
from deco.sources import Dataset
import sys
from functools import partial
import tensorflow as tf

tokenizer = ElectraTokenizerFast("/data/pubmed/model/vocab.txt")
#tokens = tokenizer.tokenize("hello world")
#res = tokenizer(tokens, is_split_into_words=True)
#print(res)

tokenizer_func = partial(tokenizer, max_length=128, truncation=True, padding='max_length', \
                return_token_type_ids=True, return_attention_mask=True)
#res = tokenizer_func("Hi. What's up.")
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)
#ds = Dataset.from_lines("abstracts/*.tsv").map(str.strip) \
#    .where(lambda a: a).map(tokenizer.tokenize).whole_word_mask().top(10)
#for item in ds:
#    print(item)
#sys.exit()
ds = Dataset.from_lines("abstracts/*.tsv").map(str.strip) \
    .where(lambda a: a).map(tokenizer_func).batch(32).map(data_collator)

def gen():
    for item in ds:
        inputs = tf.convert_to_tensor(item["input_ids"].numpy())
        labels = tf.convert_to_tensor(item["labels"].numpy())
        #yield {"input_ids": inputs}, {"output_1": labels}
        yield inputs, labels

config = ElectraConfig(vocab_size=len(tokenizer.get_vocab()))
model = TFElectraForMaskedLM(config)

#i = iter(ds)
#i = next(i)
#print(len(i["input_ids"]))
#sys.exit()
training_args = TFTrainingArguments(
    output_dir="./electra_out",
    overwrite_output_dir=True,
    num_train_epochs=1,
    #per_gpu_train_batch_size=64,
    save_steps=10_000,
    #save_total_limit=2,
)
def shape_list(x: tf.Tensor):
    """
    Deal with dynamic shape in tensorflow cleanly.
    Args:
        x (:obj:`tf.Tensor`): The tensor we want the shape of.
    Returns:
        :obj:`List[int]`: The shape of the tensor as a list.
    """
    static = x.shape.as_list()
    dynamic = tf.shape(x)
    return [dynamic[i] if s is None else s for i, s in enumerate(static)]
class MyLoss(tf.keras.losses.Loss):
    def call(self, labels, logits):
        print(labels)
        loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True, reduction=tf.keras.losses.Reduction.NONE
        )
        # make sure only labels that are not equal to -100
        # are taken into account as loss
        active_loss = tf.not_equal(tf.reshape(labels, (-1,)), -100)
        reduced_logits = tf.boolean_mask(tf.reshape(logits, (-1, shape_list(logits)[2])), active_loss)
        labels = tf.boolean_mask(tf.reshape(labels, (-1,)), active_loss)
        return loss_fn(labels, reduced_logits)
    
#import tensorflow_addons as tfa
optimizer,lr = create_optimizer(1e-4,1000000,10000,0.1,1e-6,0.01)
training_loss = TFMaskedLanguageModelingLoss.compute_loss
model.compile(optimizer=optimizer, loss=MyLoss())
model.fit(gen(), callbacks=[tf.keras.callbacks.TensorBoard(log_dir="./log", update_freq='batch', profile_batch=0),
                tf.keras.callbacks.ModelCheckpoint("./output/model_{epoch}", save_freq=200000)])
#model.summary()
#trainer = TFTrainer(
#    model=model,
#    args=training_args,
#    train_dataset=gen(),
#    prediction_loss_only=True,
#)

#trainer.train()