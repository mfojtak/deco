from tokenizers import Tokenizer
from transformers import ElectraTokenizer, TFElectraPreTrainedModel, \
        ElectraConfig, PreTrainedModel, TFElectraForMaskedLM, TFElectraForPreTraining, \
            TFElectraModel, TFPreTrainedModel, pipeline
import numpy as np
from deco.sources import Dataset
import deco
import sys

tokenizer = ElectraTokenizer("model/vocab.txt")
config = ElectraConfig.from_json_file("output/generator_pretrained/config.json")
model = TFElectraForMaskedLM.from_pretrained("output/generator_pretrained/")
masked = pipeline("fill-mask", model=model, tokenizer=tokenizer, framework="tf", device=1)
res = masked("Coronaviruses are a group of RNA viruses that cause diseases in mammals and birds.")
print(res)
sys.exit()


tokenizer = Tokenizer.from_file("tokenizer.json")
def tokenize(item):
    encoded = tokenizer.encode(item)
    return encoded.tokens

def encode(item):
    res = []
    for token in item:
        res.append(tokenizer.token_to_id(token))
    return res
    #encoded = tokenizer.encode(item.tolist(), is_pretokenized=True)
    #if len(item) != len(encoded.ids):
    #    print(item.tolist() + encoded.type_ids)
    #    sys.exit()
    #return encoded.ids
#.pad(0, length=128, axis=1) \
text = Dataset.from_lines("abstracts/*.tsv").split_by("\n").map(tokenize, axis=1) \
    .concat(max_len=126, axis=1)
#.map(str.strip, axis=1) \
#    .map(tokenize, axis=1).concat(max_len=126, axis=1)
mask = text.whole_word_mask()
encoded = text.map(encode, axis=0)
masked = encoded.where(mask.logical_not(), 4).pad((2,3)).pad(0, length=128)
output = encoded.where(mask, encoded.full_like(-100)).pad((-100,-100)).pad(-100, length=128)
res = masked.zip(output).batch(32).transpose()
for item in res.top(2):
    print(item)

sys.exit()

#    .pad(("[CLS]", "[SEP]"), axis=1).map(encode, axis=1).pad(0, length=128, axis=1) \
#    .batch(2).transpose().top(10)
for item in ds:
    print(item)
sys.exit()
tt = Dataset.create([[["ab", "b"], ["c", "dd"]], [["e", "f", "g"], [1], [2]]]).concat(axis=1, max_len=4)
for item in tt:
    print(item)

tokenizer = Tokenizer.from_file("tokenizer.json")
encoded = tokenizer.encode("I can feel the magic, can you? Ostrava")
print(encoded.tokens, encoded.ids, encoded.overflowing)