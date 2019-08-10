import tensorflow as tf
import tf_sentencepiece as tfs
import sys
import collections


class SentencepieceTokenizer(tf.keras.layers.Layer):

    def __init__(self, tokenizer, unk_id=0):
        super(SentencepieceTokenizer, self).__init__()
        if isinstance(tokenizer, str):
            self.tokenizer = open(tokenizer, "rb").read()
        else:
            self.tokenizer = tokenizer
        self.unk_id = 0

    def call(self, texts):
        pieces, lengths = tfs.encode_dense(
            texts, model_proto=self.tokenizer)
        pieces = tf.where(tf.equal(pieces, 0), self.unk_id, pieces)
        pieces = tf.RaggedTensor.from_tensor(pieces, lengths=lengths)
        return pieces

    def get_config(self):
        return {'tokenizer': self.tokenizer, 'unk_id': self.unk_id}


#tok = SentencepieceTokenizer("/data/develop/sp_unigram_small.model")
#res = tok(["hello world", "what's up"])
#print(res)