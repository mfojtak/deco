import sentencepiece as spm
import collections
import tensorflow as tf
import codecs
import numpy as np

class SentencepieceTokenizer(object):
  """Runs end-to-end tokenziation."""

  def __init__(self, vocab_file, model_file, do_lower_case=True):
    self.vocab = self.load_vocab(vocab_file)
    self.inv_vocab = {v: k for k, v in self.vocab.items()}
    self.sp = spm.SentencePieceProcessor()
    self.sp.Load(model_file)
    self.unk_token = "[UNK]"
    self.cls_id = self.vocab["[CLS]"]
    self.sep_id = self.vocab["[SEP]"]

  def load_vocab(self, vocab_file):
    """Loads a vocabulary file into a dictionary."""
    res = collections.OrderedDict()
    index = 0
    with codecs.open(vocab_file, 'r', 'utf8') as reader:
        while True:
            token = reader.readline()
            if not token:
                break
            token = token.strip().split()[0]
            res[token] = index
            index += 1
    for special_token in ['[PAD]','[UNK]','[CLS]','[SEP]','[MASK]']:
        token = special_token
        if token not in res:
            res[token] = index
            index += 1
    return res

  def special_tokens(self):
    return ['[PAD]','[UNK]','[CLS]','[SEP]','[MASK]', "<unk>", "<s>", "</s>"]

  def convert_by_vocab(self, vocab, items):
    """Converts a sequence of [tokens|ids] using the vocab."""
    output = []
    for item in items:
      output.append(vocab[item])
    return output

  def tokenize_batch(self, batch):
    res = []
    for t in batch:
      res.append(self.tokenize(t))
    return res

  def tokenize(self, text):
    output_ids = self.sp.EncodeAsIds(text)
    output_tokens = [self.sp.IdToPiece(i)
                    if i != 0 else self.unk_token
                    for i in output_ids]
    return output_tokens

  def tokenize_bert(self, text_a, text_b=None):
      tokens_a = self.tokenize(text_a)
      tokens = ["[CLS]"] + tokens_a + ["[SEP]"]
      if text_b:
          tokens_b = self.tokenize(text_b)
          tokens = tokens + tokens_b + ["[SEP]"]
      return tokens

  def encode_bert(self, text_a, text_b=None, max_len=512):
      
      first_tokens = self.tokenize(text_a)
      first_ids = [self.cls_id] + self.tokens_to_ids(first_tokens) + [self.sep_id]
      segments = [0] * len(first_ids)
      ids = first_ids
      if text_b:
        second_tokens = self.tokenize(text_b)
        second_ids = self.tokens_to_ids(second_tokens) + [self.sep_id]
        segments += [1] * len(second_ids)
        ids += second_ids
      pad = max_len - len(ids)
      segments += [0] * pad
      ids += [0] * pad
      return ids, segments 
  
  def encode_bert_batch(self, texts_a, texts_b=None, max_len=512):
      indices = []
      segments = []
      if texts_b:
        for pair in zip(texts_a, texts_b):
            i,s = self.encode_bert(pair[0], pair[1], max_len=max_len)
            indices.append(i)
            segments.append(s)
      else:
        for text in texts_a:
            i,s = self.encode_bert(text, max_len=max_len)
            indices.append(i)
            segments.append(s)
      return indices, segments


  def tokens_to_ids(self, tokens):
    return self.convert_by_vocab(self.vocab, tokens)

  def ids_to_tokens(self, ids):
    return self.convert_by_vocab(self.inv_vocab, ids)

  
  def bert_create_pretrained(self, sentence_pairs,
                     seq_len=512,
                     mask_rate=0.15,
                     mask_mask_rate=0.8,
                     mask_random_rate=0.1,
                     swap_sentence_rate=0.5,
                     force_mask=True):
    """Generate a batch of inputs and outputs for training.
    :param sentence_pairs: A list of pairs containing lists of tokens.
    :param token_dict: The dictionary containing special tokens.
    :param token_list: A list containing all tokens.
    :param seq_len: Length of the sequence.
    :param mask_rate: The rate of choosing a token for prediction.
    :param mask_mask_rate: The rate of replacing the token to `TOKEN_MASK`.
    :param mask_random_rate: The rate of replacing the token to a random word.
    :param swap_sentence_rate: The rate of swapping the second sentences.
    :param force_mask: At least one position will be masked.
    :return: All the inputs and outputs.
    """
    batch_size = len(sentence_pairs)
    unknown_index = self.vocab[self.unk_token]
    spec_tokens = self.special_tokens()
    token_list = list(self.vocab.keys())

    # Generate sentence swapping mapping
    nsp_outputs = np.zeros((batch_size,))
    mapping = {}
    if swap_sentence_rate > 0.0:
        indices = [index for index in range(batch_size) if np.random.random() < swap_sentence_rate]
        mapped = indices[:]
        np.random.shuffle(mapped)
        for i in range(len(mapped)):
            if indices[i] != mapped[i]:
                nsp_outputs[indices[i]] = 1.0
        mapping = {indices[i]: mapped[i] for i in range(len(indices))}
    # Generate MLM
    token_inputs, segment_inputs, masked_inputs = [], [], []
    mlm_outputs = []
    for i in range(batch_size):
        first, second = sentence_pairs[i][0], sentence_pairs[mapping.get(i, i)][1]
        segment_inputs.append(([0] * (len(first) + 2) + [1] * (seq_len - (len(first) + 2)))[:seq_len])
        tokens = ["[CLS]"] + first + ["[SEP]"] + second + ["[SEP]"]
        tokens = tokens[:seq_len]
        tokens += ["<unk>"] * (seq_len - len(tokens))
        token_input, masked_input, mlm_output = [], [], []
        has_mask = False
        for token in tokens:
            mlm_output.append(self.vocab.get(token, unknown_index))
            if token not in spec_tokens and np.random.random() < mask_rate:
                has_mask = True
                masked_input.append(1)
                r = np.random.random()
                if r < mask_mask_rate:
                    token_input.append(self.vocab["[MASK]"])
                elif r < mask_mask_rate + mask_random_rate:
                    while True:
                        token = np.random.choice(token_list)
                        if token not in spec_tokens:
                            token_input.append(self.vocab[token])
                            break
                else:
                    token_input.append(self.vocab.get(token, unknown_index))
            else:
                masked_input.append(0)
                token_input.append(self.vocab.get(token, unknown_index))
        if force_mask and not has_mask:
            masked_input[1] = 1
        token_inputs.append(token_input)
        masked_inputs.append(masked_input)
        mlm_outputs.append(mlm_output)
    inputs = [np.asarray(x) for x in [token_inputs, segment_inputs, masked_inputs]]
    outputs = [np.asarray(np.expand_dims(x, axis=-1)) for x in [mlm_outputs, nsp_outputs]]
    return inputs, outputs


#tok = SentencepieceTokenizer(vocab_file="/data/BioNLP/BERT/sp_bpe.vocab", model_file="/data/BioNLP/BERT/sp_bpe.model")
#tokens = tok.tokenize("hypertension problem")
#ids = tok.convert_tokens_to_ids(tokens)
#print(tokens, ids)
