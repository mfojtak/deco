import pyarrow as pa
import pyarrow.parquet as pq
from deco.sources import Dataset
import sys
import numpy as np

class ParquetWriter:
    def __init__(self, parent, filename, column_names = None):
        self.filename = filename
        self.parent = parent
        self.column_names = column_names
    def run(self):
        writer = None
        for batch in self.parent:
            data = []
            if not self.column_names:
                self.column_names = []
                for i in range(0, len(batch)):
                    self.column_names.append("col{}".format(i))
            for column in batch:
                arr = pa.array(list(column))
                data.append(arr)
            table = pa.Table.from_arrays(data, self.column_names)
            if not writer:
                writer = pq.ParquetWriter(self.filename, table.schema)
            writer.write_table(table)
        writer.close()

def write_parquet(self, filename, column_names=None):
    return ParquetWriter(self, filename, column_names)

Dataset.write_parquet = write_parquet