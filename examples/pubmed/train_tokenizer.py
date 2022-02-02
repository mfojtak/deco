#!/usr/bin/env python
import glob
import sentencepiece as spm
import random
from dask.distributed import Client
import argparse

parser = argparse.ArgumentParser(description='Trains sentencepiece tokenizer')
parser.add_argument('--files', action="store", dest="files", default="/data/develop/sentences/*")
parser.add_argument('--model_prefix', action="store", dest="model_prefix", default="sp_unigram_large")
parser.add_argument('--vocab_size', action="store", dest="vocab_size", default=200000)
args = parser.parse_args()

def processor():
    files = glob.glob(args.files, recursive=True)
    random.shuffle(files)
    files = files[0:70]
    files_str = ",".join(files)
    print(files_str)

    command = '--input={} --model_prefix={} --shuffle_input_sentence=true --vocab_size={} --hard_vocab_limit=false --model_type=unigram'.format(files_str, args.model_prefix, args.vocab_size)
    spm.SentencePieceTrainer.Train(command)

if __name__ == '__main__':
    #cluster = KubeCluster.from_yaml('memory-worker-spec.yaml')
    #cluster.scale_up(1)
    #client = Client(cluster)
    #future = client.submit(processor)
    processor()
