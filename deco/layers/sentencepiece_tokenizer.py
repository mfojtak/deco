import tensorflow as tf
import tensorflow_text as text
import sys
import collections
import base64


class SentencepieceTokenizer(tf.keras.layers.Layer):

    def __init__(self, model=None, model_path=None):
        super(SentencepieceTokenizer, self).__init__()
        if model_path:
            self.proto = open(model_path, "rb").read()
        if model:
            if isinstance(model, str):
                asc_str = model.encode("ascii")
                self.proto = base64.decodebytes(asc_str)
            if isinstance(model, bytes):
                self.proto = model
        self.tokenizer = text.SentencepieceTokenizer(self.proto)

    def call(self, texts):
        res = self.tokenizer.tokenize(texts)
        return res

    def get_config(self):
        encoded = base64.encodebytes(self.proto)
        asc = encoded.decode('ascii')
        return {'model': asc}
    
    def vocab_size(self):
        return self.tokenizer.vocab_size()


#proto = open("/data/pubmed/sp_unigram_small.model", "rb").read()
#tok = SentencepieceTokenizer(model_path="/data/pubmed/sp_unigram_small.model")
#print(tok.vocab_size())
#res = tok(["hello world", "what's up"])
#print(res)
#tf.saved_model.save(tok, "/data/deco/tmp")

#tokenizer = text.WhitespaceTokenizer()
#tokens = tokenizer.tokenize(['everything not saved will be lost.'])
#print(tokens.to_list())


#tokenizer = text.SentencepieceTokenizer(proto, tf.string)
#print(tokenizer.vocab_size())
#tokens = tokenizer.tokenize(['everything not saved will be lost.'])
#print(tokens.to_list())
