from deco.sources import Dataset
import csv

class CSVReader(Dataset):
    def __init__(self, path):
        self.path = path
    async def __aiter__(self):
        with open(self.path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                yield row