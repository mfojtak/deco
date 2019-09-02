from deco.sources import Dataset
import csv
import glob

class CSVReader(Dataset):
    def __init__(self, files):
        self.files = files
    async def __aiter__(self):
        files_list = glob.glob(self.files)
        for file_path in files_list:
            with open(file_path) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    yield row