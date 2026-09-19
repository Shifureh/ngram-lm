import sqlite3
from operator import itemgetter
import random
import re

conn = sqlite3.connect("ngrams.db")
cursor = conn.cursor()

MAX_WORDS = 7
P_WORD_LIMIT = 0.9

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

    if (n_length <= 1):
        return {}
    
    # if nothing exists return empty dictionary
    if not all_rows:
        context_list = context.split(" ")
        context_list.pop(0)

        context_string = " ".join(context_list)
        next_word_probablities = get_probabilities(context_string, n_length - 1)

    return next_word_probablities

def apply_p_word_sampling(next_word_probablities, limit):

    # sorts values greatest to smallest
    sorted_probabilities = dict(sorted(next_word_probablities.items(), key=itemgetter(1), reverse=True))
    smaller_probabilities = {}

    sum = 0
    for (key, value) in sorted_probabilities.items():
        if (sum >= limit):
            break
        else: 
            sum = sum + value
            smaller_probabilities.update({key: value})

    # renormalized data by the current "total"
    for (key, value) in smaller_probabilities.items():
        smaller_probabilities.update({key: value / sum})

    return smaller_probabilities

def generate_next_word(probabilites, sampled_num, context_input_list):

    word_list = []
    probabilities_list = []
    new_context_list = []

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
            new_context_list = update_context(context_input_list, word_list[count])
            return word_list[count], count, current_range, new_context_list # count & range for testing

        count += 1

    return word_list[count], count, current_range, new_context_list # count & range for testing

# updates the current context input list with the newly generated word
def update_context(context_input_list, new_word):

    temp_list = context_input_list
    context_length = len(context_input_list)
    context_input_list = [None] * context_length

    count = 0
    for item in temp_list:

        if (count == context_length - 1):
            context_input_list[count] = new_word
        else: 
            context_input_list[count] = temp_list[count + 1]
        
        count += 1

    return context_input_list


# gets starting context with error handling
while True:
    try:
        context_input = input("Enter up to 3 words to start generating: ")
        context_input_list = re.findall(r"\w+(?:'\w+)?|[.,]", context_input.lower())
        if len(context_input_list) > 3:
            print("Too many words, try again.")
        else:
            break
    except ValueError:
        print("Invalid Input, try again")


# gets n-length gram
n_length = 1
for token in context_input_list:
    n_length += 1

generated_sentence_list = list(context_input_list)   # full growing output
current_context_list = list(context_input_list)      # fixed-size sliding window

has_period = False

while len(generated_sentence_list) < MAX_WORDS and not has_period:

    context_string = " ".join(current_context_list)
    probabilities = get_probabilities(context_string, n_length)
    smaller_sorted_probabilities = apply_p_word_sampling(probabilities, P_WORD_LIMIT)

    if not probabilities:
        print("No data found. Try a different phrase.")
        break
    else:
        sampled_num = random.random()
        next_word, next_word_index, curr_range, new_context_list = generate_next_word(smaller_sorted_probabilities, sampled_num, current_context_list)

        generated_sentence_list.append(next_word)
        current_context_list = new_context_list

        if next_word == ".":
            has_period = True


print(" ".join(generated_sentence_list))


# # first round of generation
# context_string = " ".join(context_input_list)
# probabilities = get_probabilities(context_string, n_length)

# if not probabilities:
#     print("No data found for this context. Try a different phrase.")
# else:
#     sampled_num = random.random()
#     next_word = ""
#     next_word_index = 0 # testing
#     curr_range = [] # testing
#     new_context_list = []
#     next_word, next_word_index, curr_range, new_context_list = generate_next_word(probabilities, sampled_num, context_input_list)
#     generated_sentence_list.append(next_word)
#     print(new_context_list)












# testing
# for key, value in probabilities.items():
#     print(key, value)

# sampled_num = random.random()
# next_word = ""
# next_word_index = 0 # testing
# curr_range = [] # testing
# next_word, next_word_index, curr_range = generate_next_word(probabilities, sampled_num)

# # testing
# count = 0
# for key, value in probabilities.items():
#     print(f"{count}: {key}") 
#     count += 1

# print("the next word is: " + next_word)
# print(f"word index: {next_word_index}")
# print(f"sampleded num: {sampled_num}")
# print(f"range: {curr_range}")

    