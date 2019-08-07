#!/usr/bin/env python
from flask import Flask, request, jsonify
import numpy as np
import deco
import requests
import csv
import json
import argparse

parser = argparse.ArgumentParser(description='Exports keras model to serving format')
parser.add_argument('--port', action="store", dest="port", default=4000)
parser.add_argument('--vocab_path', action="store", dest="vocab_path")
parser.add_argument('--model_path', action="store", dest="model_path")
parser.add_argument('--serving_url', action="store", dest="serving_url")
parser.add_argument('--static_folder', action="store", dest="static_folder", default="./static")

args = parser.parse_args()

tokenizer = deco.tokenizers.SentencepieceTokenizer(args.vocab_path, args.model_path)

app = Flask(__name__, static_folder=args.static_folder', static_url_path="/static")
SEQ_LEN = 128

def get_features(content):
    result = []
    for text in content["texts"]:
        if isinstance(text, str):
            first = text
            second = None
        else:
            first = text["first"]
            second = text["second"]
        indices, segments = tokenizer.encode_bert(first, second, max_len=SEQ_LEN)
        result.append({"Input-Token": indices, "Input-Segment": segments})
    return result

@app.route('/predict', methods=['POST'])
def bert_predict():
    content = request.json
    features = get_features(content)
    model = content["model"]
    model_url = "{}/v1/models/{}:predict".format(args.serving_url, model)
    pred_res = requests.post(model_url, json={"instances": features})

    return pred_res.text

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True,port=args.port)
