import tensorflow as tf
import tf_sentencepiece as tfs
import sys
import collections
import json
import base64


@tf.function
def pad(x, limit):
    ll = limit - x.row_lengths()
    count = tf.math.reduce_sum(ll)
    pad = tf.RaggedTensor.from_row_lengths(
        values=tf.zeros([count], dtype=x.dtype), row_lengths=ll)
    res = tf.concat([x, pad], axis=1).to_tensor()
    res.set_shape((x.shape[0], limit))
    return res


class BertInput(tf.keras.layers.Layer):

    def __init__(self, tokenizer=None, tokenizer_path=None, max_length=128):
        super(BertInput, self).__init__()
        if tokenizer_path:
            self.tokenizer = open(tokenizer_path, "rb").read()
        if tokenizer:
            asc_str = tokenizer.encode("ascii")
            self.tokenizer = base64.decodebytes(asc_str)
        self.max_length = max_length
        vocab_len = tfs.piece_size(model_proto=self.tokenizer)
        self.pad_id = vocab_len
        self.unk_id = vocab_len + 1
        self.cls_id = vocab_len + 2
        self.sep_id = vocab_len + 3
        self.mask_id = vocab_len + 4

    def call(self, texts):
        if isinstance(texts, collections.Sequence):
            texts_a = texts[0]
        else:
            texts_a = texts
        pieces_a, lengths_a = tfs.encode_dense(
            texts_a, model_proto=self.tokenizer)
        pieces_a = tf.where(tf.equal(pieces_a, 0), self.unk_id, pieces_a)
        pieces_a = tf.RaggedTensor.from_tensor(pieces_a, lengths=lengths_a)
        cls_ids = tf.fill([pieces_a.nrows(), 1], self.cls_id)
        sep_ids = tf.fill([pieces_a.nrows(), 1], self.sep_id)
        merged_a = tf.concat([cls_ids, pieces_a, sep_ids], axis=1)
        tokens = merged_a
        segments = tf.zeros_like(merged_a)
        if isinstance(texts, collections.Sequence):
            pieces_b, lengths_b = tfs.encode_dense(
                texts[1], model_proto=self.tokenizer)
            pieces_b = tf.where(tf.equal(pieces_b, 0), self.unk_id, pieces_b)
            pieces_b = tf.RaggedTensor.from_tensor(pieces_b, lengths=lengths_b)
            merged_b = tf.concat([pieces_b, sep_ids], axis=1)
            tokens = tf.concat([tokens, merged_b], axis=1)
            segments = tf.concat([segments, tf.ones_like(merged_b)], axis=1)
        return pad(tokens, self.max_length), pad(segments, self.max_length)

    def get_config(self):
        encoded = base64.encodebytes(self.tokenizer)
        asc = encoded.decode('ascii')
        return {'tokenizer': asc, 'max_length': self.max_length}

    # def compute_output_shape(self, input_shape):
    #  return ((input_shape[0], self.max_length), (input_shape[0], self.max_length))


#encoded = base64.encodebytes(b"hello")
#encoded_asc = encoded.decode('ascii')

#t = encoded_asc.encode('ascii')

#decoded = base64.decodebytes(t)
#print(encoded, encoded_asc, decoded)
#sys.exit()


#layer = BertInput(tokenizer_path="/data/develop/sp_unigram_small.model")
#conf = layer.get_config()
#del layer
#layer = BertInput.from_config(conf)

#texts_a = tf.constant(["this is string", "and other"])
#texts_b = tf.constant(["this is new string", "so"])
#t, s = layer((texts_a, texts_b))
#print(t, s)