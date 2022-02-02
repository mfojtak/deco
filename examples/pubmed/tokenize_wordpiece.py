print("Training tokenizer")
from tokenizers import BertWordPieceTokenizer

import glob
import random

files = glob.glob("/data/pubmed/abstracts/*.tsv", recursive=True)
random.shuffle(files)
tokenizer_files = files[0:200]
print(tokenizer_files)

tokenizer = BertWordPieceTokenizer()
tokenizer.train(files=tokenizer_files)
tokenizer.save("tokenizer.json", pretty=True)

