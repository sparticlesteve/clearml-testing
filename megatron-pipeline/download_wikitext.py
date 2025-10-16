import os
import argparse
from datasets import load_dataset
from transformers import GPT2TokenizerFast
from clearml import Task

# Get current task (created by the bash wrapper task)
task = Task.init(project_name="Megatron testing",
                 task_name="download-data-step")

scratch = os.environ.get('SCRATCH')
default_data_dir = f"{scratch}/data/wikitext" if scratch else "./data/wikitext"

parser = argparse.ArgumentParser()
parser.add_argument("--data-dir",
                    default=default_data_dir,
                    help="Root directory for data storage")
args = parser.parse_args()
DATA_DIR = args.data_dir

# set hf home and make data dir
os.makedirs(DATA_DIR, exist_ok=True)

# tokenization rules
TOKENIZER_DIR = os.path.join(DATA_DIR, "tokenizer_gpt2")
os.makedirs(TOKENIZER_DIR, exist_ok=True)

# download
print("Downloading WikiText-103...")
dataset = load_dataset("Salesforce/wikitext",
                       "wikitext-103-v1",
                       cache_dir=DATA_DIR)

# save as json lines (megatron takes json by default)
print("Saving dataset as JSON lines...")
dataset['train'].to_json(os.path.join(DATA_DIR, "wikitext103_train.json"),
                         orient="records", lines=True)
dataset['validation'].to_json(os.path.join(DATA_DIR, "wikitext103_valid.json"),
                              orient="records", lines=True)
dataset['test'].to_json(os.path.join(DATA_DIR, "wikitext103_test.json"),
                        orient="records", lines=True)

# download tokenizer
print("Downloading GPT-2 tokenizer...")
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
tokenizer.save_pretrained(TOKENIZER_DIR)

#task.upload_artifact('data_dir', DATA_DIR)
#task.upload_artifact('tokenizer_dir', TOKENIZER_DIR)

print('Done')
