import deco.sources.dataset
from abc import ABC, abstractmethod
from copy import deepcopy

class Context:
    def __init__(self):
        self._nodes = []
    @abstractmethod
    def add_node(self, node):
        self._nodes.append(node)
    def __enter__(self):
        deco.sources.dataset._current_context=self
    def __exit__(self, type, value, traceback):
        self.process()
        deco.sources.dataset._current_context=None
    @abstractmethod
    def process(self):
        pass
    

class ParallelContext(Context):
    def __init__(self, workers=None):
        super().__init__()
        self._workers = workers
        self._group = 0
        self._node_group = {}

    def add_node(self, node):
        super().add_node(node)
        self._node_group[node] = self._group

    def process(self):
        inp_proxy = {}
        nodes_copy = self._nodes.copy()
        for node in nodes_copy:
            for i, inp in enumerate(node._inputs):
                if not any(id(inp) == id(n) for n in nodes_copy):
                    if inp in inp_proxy.keys():
                        proxy = inp_proxy[inp]
                    else:
                        proxy = deco.sources.Slice(inp, 0, None, 2)
                        proxy._deepcopy_input = False
                        inp_proxy[inp] = proxy
                    node._inputs[i] = proxy
                    node._iters[i] = proxy
        for node in nodes_copy:
            if len(node._outputs) == 0:
                self._cache = deco.sources.Cache(node)
        self._copies = [self._cache]
        self._group = 1
        new_copy = deepcopy(self._cache)
        self._copies.append(new_copy)
        for node in self._node_group.keys():
            node._group = self._node_group[node]
            #if isinstance(node, deco.sources.Slice) and node._deepcopy_input:

            

    def __call__(self):
        return self._copies
        

