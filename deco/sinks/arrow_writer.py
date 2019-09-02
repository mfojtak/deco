import pyarrow as pa
from deco.sources import Dataset

class ArrowWriter:
    def __init__(self, parent, filename):
        self.filename = filename
        self.parent = parent
    async def run(self):
        stream = pa.output_stream(self.filename)
        async for item in self.parent:
            buf = pa.serialize(item).to_buffer()
            stream.write(buf)
        stream.close()

def write_arrow(self, filename):
    return ArrowWriter(self, filename)

Dataset.write_arrow = write_arrow