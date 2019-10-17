import pyarrow as pa
from deco.sources import Dataset
from deco.sinks import Sink

class TensorWriter(Sink):
    def __init__(self, parent, filename):
        self.filename = filename
        self.parent = parent
    def __iter__(self):
        stream = pa.output_stream(self.filename)
        for item in self.parent:
            tensor = pa.Tensor.from_numpy(item)
            pa.write_tensor(tensor, stream)
            yield
        stream.close()

def write_tensor(self, filename):
    return TensorWriter(self, filename)

Dataset.write_tensor = write_tensor