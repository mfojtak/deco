import deco
import tf_sentencepiece as tfs

def get_custom_objects():
    ret = {"Mapper": deco.layers.Mapper,
           "BertInput": deco.layers.BertInput}
    return ret
