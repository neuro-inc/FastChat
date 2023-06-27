import os

from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import TrainingArguments
from transformers import TrainingArguments, Trainer
import numpy as np
import evaluate


cache_root = os.environ['CACHE_ROOT']
results_root = os.environ['CACHE_ROOT']
dataset_dir = cache_root + '/huggingface/datasets'
model_cache_dir = cache_root + '/huggingface/models'
output_dir = results_root + '/result'
evaluate_cache = cache_root + '/huggingface/evaluate'


dataset = load_dataset("yelp_review_full", data_dir=dataset_dir)
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")


def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)


tokenized_datasets = dataset.map(tokenize_function, batched=True)

small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000))

model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=5, cache_dir=model_cache_dir)
training_args = TrainingArguments(output_dir=output_dir)

metric = evaluate.load("accuracy", cache_dir=evaluate_cache)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments(output_dir=output_dir, evaluation_strategy="epoch")

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train_dataset,
    eval_dataset=small_eval_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()
