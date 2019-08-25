import pyarrow as pa
import pyarrow.parquet as pq
from deco.sources import Dataset

class ParquetWriter:
    def __init__(self, parent, filename, column_names = None):
        self.filename = filename
        self.parent = parent
        self.column_names = column_names
    async def run(self):
        writer = None
        async for batch in self.parent:
            data = []
            if not self.column_names:
                self.column_names = []
                for i in range(0, len(batch)):
                    self.column_names.append("col{}".format(i))
            for column in batch:
                data.append(pa.array(column))
            table = pa.Table.from_arrays(data, self.column_names)
            if not writer:
                writer = pq.ParquetWriter(self.filename, table.schema)
            writer.write_table(table)
        writer.close()

def write_parquet(self, filename, column_names=None):
    return ParquetWriter(self, filename, column_names)

Dataset.write_parquet = write_parquet