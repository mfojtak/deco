import pyarrow as pa
from deco.sources import Dataset

class TensorReader(Dataset):
    def __init__(self, path):
        self.path = path
    def __iter__(self):
        input_stream = pa.input_stream(self.path)
        while(True):
            try:
                result = pa.read_tensor(input_stream)
                yield result.to_numpy()
            except:
                break
        input_stream.close()

def from_tensor(path):
    return TensorReader(path)

Dataset.from_tensor = from_tensor