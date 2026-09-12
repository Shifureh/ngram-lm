import sqlite3
from collections import Counter
from preprocess_text import load_all_texts, tokenize_all


def generate_ngrams(tokens, n):
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
    for n in range(2,5):
        for filepath, tokens in tokenized_texts.items():
            print(f"Processing {filepath} for {n}-grams...")
            ngrams = generate_ngrams(tokens, n)
            counts = Counter(ngrams)
            save_ngrams(n, conn, counts)

    print("n-grams inserted successfully")

    # testing
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM ngrams;")
    rows = cursor.fetchone()[0]
    print(f"Total rows in n-gram table: {rows}")

    cursor.execute(
        """
        SELECT context, next_word, count 
        FROM ngrams 
        ORDER BY count DESC 
        LIMIT 5;
        """
    )
    print("\n5 most frequent n-grams:")
    for context, next_word, count in cursor.fetchall():
        print(f"'{context}' -> '{next_word}': {count}")


    cursor.execute(
        """
        SELECT n_length, COUNT(*) AS unique_contexts, AVG(count) AS avg_count
        FROM ngrams
        GROUP BY n_length;
        """
    )
    print("\nSummary of n-grams:")
    for n_length, unique_contexts, avg_count in cursor.fetchall():
        print(
            f"{n_length}-grams: {unique_contexts} unique contexts, average count: {avg_count:.2f}"
        )


    cursor.execute(
        """
        SELECT SUM(COUNT) FROM ngrams;
        """
    )

    total_count = cursor.fetchone()[0]
    print(f"\nTotal count of all n-grams: {total_count}")


    conn.close()


if __name__ == "__main__":
    main()