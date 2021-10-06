from deco.sources import Dataset
from deco.sources import graph
import multiprocessing
import numpy as np
import copy


class Parallel(Dataset):
    def __init__(self, node: Dataset, workers=None):
        self.node = node
        self.node._outputs.remove(self)
        self.graph = Graph(node)
        self.workers = workers
        if workers == None:
            self.workers = multiprocessing.cpu_count()
    def __iter__(self):
        print(self.graph.inputs())
        print(self.graph.outputs())
        data = self.graph.inputs()[0].get_data()
        #chunks = np.array_split(data,self.workers)
        chunks = []
        for i in range(self.workers):
            chunk = data[i::self.workers]
            chunks.append(chunk)
        iters = []
        for chunk in chunks:
            subgraph = copy.deepcopy(self.node)
            subgraph = subgraph.cache()
            subgraph_input = Graph(subgraph).inputs()[0]
            subgraph_input.set_data(chunk)
            iters.append(iter(subgraph))
        while iters:
            for i in iters.copy():
                try:
                    item = next(i)
                    yield item
                except StopIteration:
                    iters.remove(i)



def parallel_inst(self):
    return Parallel(self)

Dataset.parallel = parallel_inst