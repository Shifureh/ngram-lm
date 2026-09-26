import sqlite3
from collections import Counter
from preprocess_text import load_all_texts, tokenize_all
from fetch_gutenberg import fetch_all_books


def generate_ngrams(tokens, n):
    for i in range(len(tokens) - n + 1):
        yield tuple(tokens[i : i + n])
    

def init_db(db_path="ngrams.db", schema_path="schema.sql"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA synchronous = OFF;")
    cursor.execute("PRAGMA journal_mode = MEMORY;")
    cursor.execute("PRAGMA cache_size = 100000;")
    cursor.execute("PRAGMA temp_store = MEMORY;")

    with open(schema_path, "r", encoding="utf-8") as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    return conn


def save_ngrams(n, conn, ngram_counts, batch_size=250_000):
    cursor = conn.cursor()
    insert_sql = "INSERT INTO ngrams (n_length, context, next_word, count) VALUES (?, ?, ?, ?);"
    
    cursor.execute("BEGIN TRANSACTION;")
    batch = []
    for ngram, count in ngram_counts.items():
        batch.append((n, " ".join(ngram[:-1]), ngram[-1], count))
        if len(batch) >= batch_size:
            cursor.executemany(insert_sql, batch)
            batch.clear()

    if batch:
        cursor.executemany(insert_sql, batch)
        batch.clear()
        
    conn.commit()


def main():
    fetch_all_books()
    raw_texts = load_all_texts("data")
    tokenized_texts = tokenize_all(raw_texts)
    conn = init_db("ngrams.db", "schema.sql")
    for n in range(2,5):
        total_count_mem = Counter()
        for filepath, tokens in tokenized_texts.items():
            print(f"Processing {filepath} for {n}-grams...")
            total_count_mem.update(generate_ngrams(tokens, n))
        save_ngrams(n, conn, total_count_mem)

    print("n-grams inserted successfully")

    # testing
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA cache_size = -128000;")
    cursor.execute("PRAGMA temp_store = FILE;")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_n_length ON ngrams(n_length, count DESC);")
    conn.commit()

    for n in (2, 3, 4):
        cursor.execute(
            """
            SELECT context, next_word, count 
            FROM ngrams
            WHERE n_length = ?
            ORDER BY count DESC
            LIMIT 5;
            """,
            (n,),
        )
        print(f"\nMost frequent {n}-grams:")
        for context, next_word, count in cursor.fetchall():
            print(f"'{context}' -> '{next_word}': {count:,}")

    cursor.execute(
        """
        SELECT 
            n_length, 
            COUNT(*) AS unique_contexts, 
            AVG(count) AS avg_count,
            SUM(count) AS total_count
        FROM ngrams
        GROUP BY n_length;
        """
    )
    summary_rows = cursor.fetchall()
    
    total_unique_rows = sum(r[1] for r in summary_rows)
    total_token_occurrences = sum(r[3] for r in summary_rows)

    print("\nSummary of n-grams:")
    for n_length, unique_contexts, avg_count, _ in summary_rows:
        print(
            f"{n_length}-grams: {unique_contexts:,} unique contexts, average count: {avg_count:.2f}"
        )

    print(f"\nTotal rows in n-gram table: {total_unique_rows:,}")
    print(f"Total count of all n-grams: {total_token_occurrences:,}")

    conn.close()


if __name__ == "__main__":
    main()