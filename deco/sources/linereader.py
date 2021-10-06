from deco.sources import Dataset
import glob, random
from typing import Union
from collections.abc import Iterable

class LineReader(Dataset):
    def __init__(self, files: Iterable, shuffle_files: bool=False):
        self.files = files
        self.shuffle = shuffle_files
    def __iter__(self):
        if self.shuffle:
            random.shuffle(self.files)
        for file_path in self.files:
            print("processing {}".format(file_path))
            with open(file_path, "r") as f:
                for line in f:
                    yield line
    def get_data(self):
        return self.files
    def set_data(self, data):
        self.files = data

def from_lines(files: Union[str, Iterable], shuffle_files: bool=False):
    return LineReader(files, shuffle_files)

Dataset.from_lines = from_lines