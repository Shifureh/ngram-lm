import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocess_text import load_all_texts, tokenize_all

raw_texts = load_all_texts("data")
tokenized_texts = tokenize_all(raw_texts)


unique_words = set()

for file_tokens in tokenized_texts.values():
    for word in file_tokens:
        unique_words.add(word)

unique_words.add("<UNK>")

sorted_words = sorted(unique_words)
vocab = {}
current_index = 0

for word in sorted_words:
    vocab[word] = current_index
    current_index += 1

with open("neural/vocab.json", "w", encoding="utf-8") as f:
    json.dump(vocab, f)