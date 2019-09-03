from deco.sources import Dataset

class Where(Dataset):
    def __init__(self, parent, cond):
        self.parent = parent
        self.cond = cond
    async def __aiter__(self):
        async for item in self.parent:
            if self.cond(item):
                yield item

def where(self, cond):
    return Where(self, cond)

Dataset.where = where