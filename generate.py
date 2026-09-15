import sqlite3

conn = sqlite3.connect("ngrams.db")
cursor = conn.cursor()

def get_probabilities(context, n_length):

    total_count = 0
    next_word_probablities = {}
    cursor.execute("SELECT next_word, count FROM ngrams WHERE context = ? AND n_length = ?", (context, n_length))
    all_rows = cursor.fetchall()

    for row in all_rows:
        total_count += row[1]

    for row in all_rows:
        next_word = row[0]
        count = row[1]
        next_word_probablities[next_word] = count/total_count

    return next_word_probablities