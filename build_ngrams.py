import sqlite3
from collections import Counter
from preprocess_text import load_all_texts, tokenize_all


def generate_ngrams(tokens, n=2):
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def init_db(db_path="ngrams.db", schema_path="schema.sql"):
    conn = sqlite3.connect(db_path)
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    return conn


def save_ngrams(conn, ngram_counts):
    records = [
        (" ".join(ngram[:-1]), ngram[-1], count)
        for ngram, count in ngram_counts.items()
    ]
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO ngrams (context, next_word, count)
        VALUES (?, ?, ?)
        ON CONFLICT(context, next_word) 
        DO UPDATE SET count = count + excluded.count
        """,
        records,
    )
    conn.commit()


def main():
    raw_texts = load_all_texts("data")
    tokenized_texts = tokenize_all(raw_texts)

    conn = init_db("ngrams.db", "schema.sql")

    n = 2

    for filepath, tokens in tokenized_texts.items():
        print(f"Processing {filepath}...")
        ngrams = generate_ngrams(tokens, n=n)
        counts = Counter(ngrams)
        save_ngrams(conn, counts)

    print("n-grams inserted successfully")

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT * FROM ngrams;")
    rows = cursor.fetchone()
    print(rows)

    conn.close()


if __name__ == "__main__":
    main()