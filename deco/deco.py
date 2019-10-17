import deco
import tf_sentencepiece as tfs
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

def get_custom_objects():
    ret = {"Mapper": deco.layers.Mapper,
           "BertInput": deco.layers.BertInput}
    return ret

default_executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()*2)