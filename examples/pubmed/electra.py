from simpletransformers.language_modeling import LanguageModelingModel
import glob
import random

import logging


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

train_args = {
    "reprocess_input_data": False,
    "overwrite_output_dir": True,
    "num_train_epochs": 1,
    "save_eval_checkpoints": True,
    "save_model_every_epoch": False,
    "learning_rate": 5e-4,
    "warmup_steps": 10000,
    "train_batch_size": 64,
    "eval_batch_size": 128,
    "gradient_accumulation_steps": 1,
    "block_size": 128,
    "max_seq_length": 128,
    "dataset_type": "line_by_line",
    "wandb_project": "Pubmed - ELECTRA",
    "wandb_kwargs": {"name": "Electra-SMALL"},
    #"logging_steps": 100,
    "evaluate_during_training": True,
    "evaluate_during_training_steps": 50000,
    "evaluate_during_training_verbose": True,
    "use_cached_eval_features": True,
    "sliding_window": True,
    "tokenizer_name": "vocab.json",
    "generator_config": {
        "embedding_size": 128,
        "hidden_size": 256,
        "num_hidden_layers": 3,
    },
    "discriminator_config": {
        "embedding_size": 128,
        "hidden_size": 256,
    },
}

files = glob.glob("/data/pubmed/abstracts/*.tsv", recursive=True)
random.shuffle(files)

model = LanguageModelingModel(
    "electra",
    None,
    args=train_args,
    use_cuda=True
)

eval_files = files[:10]
train_files = files[10:]

model.train_model(
    train_files, eval_file=eval_files
)
