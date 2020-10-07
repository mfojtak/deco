from deco.sources import Dataset
import csv
import glob
from typing import Union
from collections.abc import Iterable

class CSVReader(Dataset):
    def __init__(self, files: Union[str, Iterable], delimiter=','):
        self.files = files
        self.delimiter = delimiter
    def __iter__(self):
        if isinstance(self.files, str):
            files_list = glob.glob(self.files)
        else:
            files_list = self.files
        for file_path in files_list:
            with open(file_path) as csvfile:
                reader = csv.reader(csvfile, delimiter=self.delimiter)
                for row in reader:
                    yield row