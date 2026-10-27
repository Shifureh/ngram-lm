import sqlite3
import preprocess_text
from fetch_gutenberg import fetch_all_books
from generate import interpolated_probability

PERP_BOOK_IDS = [2554]

fetch_all_books(PERP_BOOK_IDS, data_folder="perp_data")
raw_perp_text = preprocess_text.load_all_texts("perp_data")
tokenized_perp = preprocess_text.tokenize_all(raw_perp_text)

perp_tokens = list(tokenized_perp.values())[0]

def perp_func():

    return 0