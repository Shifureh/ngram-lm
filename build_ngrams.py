import sqlite3 
from preprocess_text import load_all_texts, tokenize_all

raw_texts = load_all_texts()
x = tokenize_all(raw_texts)


for filepath, tokens in x.items():
        print(filepath)
        print(tokens[:50])
        print("---\n")
