from deco.sources import Dataset

class Top(Dataset):
    def __init__(self, parent, top=10):
        self.parent = parent
        self.top = top

    async def __aiter__(self):
        iter = self.parent.__aiter__()
        for i in range(0,self.top):
            item = await iter.__anext__()
            yield item

def top(self, top):
    return Top(self, top)

Dataset.top = top