from deco.sources import Dataset
import glob
from typing import Union
from collections.abc import Iterable

class LineReader(Dataset):
    def __init__(self, files: Union[str, Iterable]):
        self.files = files
    def __iter__(self):
        if isinstance(self.files, str):
            files_list = glob.glob(self.files)
        else:
            files_list = self.files
        for file_path in files_list:
            with open(file_path, "r") as f:
                for line in f:
                    yield line

def from_lines(files: Union[str, Iterable]):
    return LineReader(files)

Dataset.from_lines = from_lines