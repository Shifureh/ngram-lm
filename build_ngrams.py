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


def save_ngrams(n, conn, ngram_counts):
    records = [
        (n, " ".join(ngram[:-1]), ngram[-1], count)
        for ngram, count in ngram_counts.items()
    ]
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO ngrams (n_length, context, next_word, count)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(n_length,context, next_word) 
        DO UPDATE SET count = count + excluded.count
        """,
        records,
    )
    conn.commit()


def main():
    raw_texts = load_all_texts("data")
    tokenized_texts = tokenize_all(raw_texts)
    conn = init_db("ngrams.db", "schema.sql")
    # for n in range(2,7):
    n = 2

    for filepath, tokens in tokenized_texts.items():
        print(f"Processing {filepath}...")
        ngrams = generate_ngrams(tokens, n=n)
        counts = Counter(ngrams)
        save_ngrams(n, conn, counts)

    print("n-grams inserted successfully")

    # testing
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM ngrams;")
    rows = cursor.fetchone()[0]
    print(f"Total rows in bigram table: {rows}")

    cursor.execute(
        """
        SELECT context, next_word, count 
        FROM ngrams 
        ORDER BY count DESC 
        LIMIT 1;
        """
    )
    print("\nMost frequent bigrams:")
    for context, next_word, count in cursor.fetchall():
        print(f"'{context}' -> '{next_word}': {count}")

    cursor.execute(
        """
        SELECT *
        FROM ngrams
        """
    )
    print("\nAll bigrams:")
    for n_length, context, next_word, count in cursor.fetchall():
        print(f"{n_length}: '{context}' -> '{next_word}': {count}")

    cursor.execute(
        """
        SELECT SUM(COUNT) FROM ngrams;
        """
    )

    total_count = cursor.fetchone()[0]
    print(f"\nTotal count of all bigrams: {total_count}")


    conn.close()


if __name__ == "__main__":
    main()