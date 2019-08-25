import deco
import keras_bert
import asyncio
import sys
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import contextlib

#data = [pa.array([1,2,3,4]), pa.array(["a", "b", "c", "d"])]
#batch = pa.RecordBatch.from_arrays(data, ["num", "char"])
#table = pa.Table.from_arrays(data, ["num", "char"])

#with pq.ParquetWriter('example.parquet', table.schema) as writer:
#    writer.write_table(table)

#sys.exit()

custom_objects = {**keras_bert.bert.get_custom_objects(), **deco.get_custom_objects(), 
                    "MaskedGlobalMaxPool1D": keras_bert.layers.MaskedGlobalMaxPool1D}

r = deco.sources.CSVReader("/data/do/names.csv")
m = r.map(lambda x: x[0])
b = m.batch(2)

t = deco.sources.Dataset.from_iterable([1,2,3,4,5,6]).batch(3)
u = t.map(lambda x: [y+10 for y in x])

z = t + u
#m = deco.nodes.KerasModel("vectors", path="/data/BioNLP/vectors_model.h5", custom_objects=custom_objects)
#f = deco.nodes.FaissIndex("index", vectors_file="/data/BioNLP/vectors.npy")
#p = deco.nodes.Sequence("sequence", nodes=[m,f])

#s = deco.executors.Serving("server", nodes=[m,f,p])
#s.run()

async def main():
    async for item in z:
        print(item)

asyncio.run(main())

