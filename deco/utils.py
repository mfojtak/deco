from deco.layers import Mapper, BertInput, SentencepieceTokenizer
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

def get_custom_objects():
    ret = {
            "Mapper": Mapper,
            "BertInput": BertInput,
            "SentencepieceTokenizer": SentencepieceTokenizer
           }
    return ret

default_executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()*2)