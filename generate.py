import sqlite3
import random

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

def generate_next_word(probabilites, sampled_num):

    word_list = []
    probabilities_list = []

    # separates the dictionary into separate word and probabilities list
    for key, value in probabilites.items():
        word_list.append(key)
        probabilities_list.append(value)

    current_range = [0.0, 0.0]
    count = 0

    for probability in probabilities_list:
        current_range[0] = current_range[1]
        current_range[1] = current_range[1] + probability

        if sampled_num > current_range[0] and sampled_num < current_range[1]:
            return word_list[count], count, current_range # count & range for testing

        count += 1

    return word_list[count], count, current_range # count & range for testing


# context given by user input
context_input = input("Enter two words to start generating: ")
context_input = context_input.lower()

# gets probabilites based on the current context
n_length = 3 # 3-gram
probabilities = get_probabilities(context_input, n_length)
sampled_num = random.random()

next_word = ""
next_word_index = 0 # testing
curr_range = [] # testing
next_word, next_word_index, curr_range = generate_next_word(probabilities, sampled_num)

# testing
count = 0
for key, value in probabilities.items():
    print(f"{count}: {key}") 
    count += 1

print("the next word is: " + next_word)
print(f"word index: {next_word_index}")
print(f"sampleded num: {sampled_num}")
print(f"range: {curr_range}")

    