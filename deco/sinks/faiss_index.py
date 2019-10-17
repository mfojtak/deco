import faiss
import numpy as np
from deco.sources import Dataset

class FaissIndex():
    def __init__(self, vectors, output_file):
        self.vectors = vectors
        self.output_file = output_file
        self.index = None
    def run(self):
        for vec in self.vectors:
            if not self.index:
                self.size = vec.shape[1]
                self.index = faiss.IndexFlatL2(self.size)
            self.index.add(vec)
        faiss.write_index(self.index, self.output_file)

def write_index(self, output_file):
    return FaissIndex(self, output_file)

Dataset.write_index = write_index

import threading

class FaissSearch:
    def __init__(self, path, top_k=10):
        self.path = path
        self.top_k = top_k
        self.index = None
        self.lock = threading.Lock()
    def _load(self):
        self.index = faiss.read_index(self.path)
    def __call__(self, input):
        with self.lock:
            if not self.index:
                self._load()
        D, I = self.index.search(input, self.top_k)
        return I