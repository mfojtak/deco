import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
from deco.sources import Dataset

class ParquetReader(Dataset):
    def __init__(self, path):
        self.path = path
    def __iter__(self):
        parquet_file = pq.ParquetFile(self.path)
        groups = parquet_file.num_row_groups
        for i in range(0, groups):
            table = parquet_file.read_row_group(i)
            columns = []
            for column in table:
                columns.append(np.array(column))
            if len(columns) == 1:
                columns = columns[0]
            yield columns

def from_parquet(path):
    return ParquetReader(path)

Dataset.from_parquet = from_parquet