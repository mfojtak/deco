import deco
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

def get_custom_objects():
    ret = {
            "Mapper": deco.layers.Mapper,
            "BertInput": deco.layers.BertInput,
            "SentencepieceTokenizer": deco.layers.SentencepieceTokenizer
           }
    return ret

default_executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()*2)