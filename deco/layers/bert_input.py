import tensorflow as tf
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

    def __init__(self, vocab_len, max_length=128):
        super(BertInput, self).__init__()
        self.vocab_len = vocab_len
        self.max_length = max_length
        self.unk_id = 0
        self.pad_id = vocab_len
        self.cls_id = vocab_len + 1
        self.sep_id = vocab_len + 2
        self.mask_id = vocab_len + 3

    def call(self, pieces):
        if isinstance(pieces, collections.abc.Sequence):
            pieces_a = pieces[0]
        else:
            pieces_a = pieces
        lengths_a = pieces_a.row_lengths()
        pieces_a = pieces_a.values
        pieces_a = tf.where(tf.equal(pieces_a, 0), self.unk_id, pieces_a)
        pieces_a = tf.RaggedTensor.from_row_lengths(values=pieces_a, row_lengths=lengths_a)
        cls_ids = tf.fill([pieces_a.nrows(), 1], self.cls_id)
        sep_ids = tf.fill([pieces_a.nrows(), 1], self.sep_id)
        merged_a = tf.concat([cls_ids, pieces_a, sep_ids], axis=1)
        tokens = merged_a
        segments = tf.zeros_like(merged_a)
        if isinstance(pieces, collections.abc.Sequence):
            pieces_b = pieces[1]
            lengths_b = pieces_b.row_lengths()
            pieces_b = pieces_b.values
            pieces_b = tf.where(tf.equal(pieces_b, 0), self.unk_id, pieces_b)
            pieces_b = tf.RaggedTensor.from_row_lengths(values=pieces_b, row_lengths=lengths_b)
            merged_b = tf.concat([pieces_b, sep_ids], axis=1)
            tokens = tf.concat([tokens, merged_b], axis=1)
            segments = tf.concat([segments, tf.ones_like(merged_b)], axis=1)
        return pad(tokens, self.max_length), pad(segments, self.max_length)

    def get_config(self):
        return {'vocab_len': self.vocab_len, 'max_length': self.max_length}

    # def compute_output_shape(self, input_shape):
    #  return ((input_shape[0], self.max_length), (input_shape[0], self.max_length))

#from sentencepiece_tokenizer import SentencepieceTokenizer
#tok = SentencepieceTokenizer(model_path="/data/pubmed/sp_unigram_small.model")
#pieces = tok(["hello world", "here"])
#print(pieces)
#layer = BertInput(vocab_len=20000)
#print(layer(pieces))

#encoded = base64.encodebytes(b"hello")
#encoded_asc = encoded.decode('ascii')

#t = encoded_asc.encode('ascii')

#decoded = base64.decodebytes(t)
#print(encoded, encoded_asc, decoded)
#sys.exit()


#layer = BertInput(vocab_len=20000)
#conf = layer.get_config()
#del layer
#layer = BertInput.from_config(conf)

#pieces_a = tf.ragged.constant([[1,2,3], [4,5]])
#lengths_a = pieces_a.row_lengths()
#pieces_a = pieces_a.values
#res = tf.equal(pieces_a, 3)
#pieces_a = tf.where(res, 0, pieces_a)
#print(pieces_a)
#pieces_b = tf.ragged.constant([[1,2,3,4], [6]])
#t, s = layer(pieces_a)
#print(t, s)