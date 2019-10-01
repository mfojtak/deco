from deco.sources import Dataset
import pyarrow as pa

class ArrowReader(Dataset):
    def __init__(self, path):
        self.path = path
    async def __iter__(self):
        reader = pa.input_stream(self.path)
        while True:
            buf = reader.read()
            obj = pa.deserialize(buf)
            print(reader.tell())
            yield obj
        
        reader.close()