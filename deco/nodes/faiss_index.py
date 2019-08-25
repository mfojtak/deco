import faiss
from deco.nodes import Transform
import numpy as np

class FaissIndex(Transform):
    def __init__(self, name, vectors_file, top_k=10):
        super().__init__(name)
        self.vectors_file = vectors_file
        self.top_k = top_k
    def _load(self):
        vectors = np.load(self.vectors_file)
        self.size = len(vectors[0])
        self.index = faiss.IndexFlatL2(self.size)
        self.index.add(vectors)
    def _unload(self):
        del self.index
    async def _eval(self, input):
        D, I = self.index.search(np.array(input), self.top_k)
        return I
    async def _info(self):
        res = {"is_trained": self.index.is_trained,
                "total": self.index.ntotal,
                "vector_size": self.size}
        return res