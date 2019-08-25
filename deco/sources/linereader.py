from deco.sources import Dataset

class LineReader(Dataset):
    def __init__(self, path):
        self.path = path
    async def __aiter__(self):
        with open(self.path, "r") as f:
            for line in f:
                yield line