import sys
import deco
import asyncio
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import contextlib
import collections
import keras_bert
from deco.sources import Dataset
import math
import timeit
import time
from typing import Iterable, TypeVar, Generic


test = Dataset.constant(np.ones(10000000)).batch(1000, axis=1).map(np.unique).concat(axis=0).reduce(np.unique)

tu = Dataset.create([[1,2,3,4], [5,6,7,8]]).window(2,1,axis=1).where(lambda a: len(a)==2)
tv = Dataset.create([[1,2,3,4], [5,6,7,8]]).shuffle()

tt = Dataset.create([["Sentence a. Sentence b", "Sentence c"], ["test", "test. trest"]]).split_sentence(axis=1).concat()


custom_objects = {**keras_bert.bert.get_custom_objects(), **deco.get_custom_objects(), 
                    "MaskedGlobalMaxPool1D": keras_bert.layers.MaskedGlobalMaxPool1D}
model = deco.nodes.KerasModel(path="/data/BioNLP/vectors_model.h5", custom_objects=custom_objects)
model._load()
names = deco.sources.CSVReader("/data/do/names.csv").squeeze().batch(32)
vectors = names.map(model)
merged = names + vectors
p = merged.write_parquet("example.parquet")

r = Dataset.from_parquet("example.parquet")

t = Dataset.create([[["abc"]],[2],["qwe",["tyu"]],5,6]).squeeze()
u = t.map(lambda x: [y+10 for y in x])

z = t + u

#m = deco.nodes.KerasModel("vectors", path="/data/BioNLP/vectors_model.h5", custom_objects=custom_objects)
#f = deco.nodes.FaissIndex("index", vectors_file="/data/BioNLP/vectors.npy")
#p = deco.nodes.Sequence("sequence", nodes=[m,f])

#s = deco.executors.Serving("server", nodes=[m,f,p])
#s.run()

#vectors.write_tensor("tensors.gz").eval()
#Dataset.from_tensor("tensors.gz").write_index("faiss.index").run()
arr = deco.sources.ArrowReader("example.arrow")
search = deco.sinks.FaissSearch("/data/BioNLP/faiss.index")

names = deco.sources.CSVReader("/data/do/names.csv").squeeze().eval()

res_vectors = Dataset.create([["Rectal tumor", "breast cancer"]]).map(model).map(search).lookup(names)
for vec in res_vectors:
    print(vec)
sys.exit()


p.run()
#async for a in test:
#    print(a)

start = time.time()
res = test()
print(res)
end = time.time()
print(end - start)
    


