import sqlite3
import string
from operator import itemgetter
import random
import re
import time

conn = sqlite3.connect("ngrams.db")
cursor = conn.cursor()

MAX_WORDS = 50
P_WORD_LIMIT = 0.9

# interpolation weights

FOUR_GRAM_ITP_WEIGHT = 0.70
THREE_GRAM_ITP_WEIGHT = 0.20
TWO_GRAM_ITP_WEIGHT = 0.10

def get_probabilities(context, n_length):
    # print(context + " " + str(n_length))

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
        

    return next_word_probablities


def interpolated_probability(context):

    next_word_probabilities = {}
    context_list = context.split(" ")
    context_length = len(context_list)    

    FOUR_GRAM_PROBABILITIES = {}
    THREE_GRAM_PROBABILITIES = {}
    TWO_GRAM_PROBABILITIES = {}


    if context_length == 3:
        four_gram_context = " ".join(context_list[-3:])
        # print(f"4-gram context is: {four_gram_context}")
        FOUR_GRAM_PROBABILITIES = get_probabilities(four_gram_context, 4)
        if not FOUR_GRAM_PROBABILITIES:
            context_length -= 1

    if context_length == 2:
        three_gram_context = " ".join(context_list[-2:])
        # print(f"3-gram context is: {three_gram_context}")
        THREE_GRAM_PROBABILITIES = get_probabilities(three_gram_context, 3)
        if not THREE_GRAM_PROBABILITIES:
            context_length -= 1

    if context_length == 1:
        two_gram_context = " ".join(context_list[-1:])
        # print(f"2-gram context is: {two_gram_context}")
        TWO_GRAM_PROBABILITIES = get_probabilities(two_gram_context, 2)
    

    all_candidates = set(FOUR_GRAM_PROBABILITIES) | set(THREE_GRAM_PROBABILITIES) | set(TWO_GRAM_PROBABILITIES)

    for key in all_candidates:
        next_word_probabilities[key] = (
            FOUR_GRAM_ITP_WEIGHT * FOUR_GRAM_PROBABILITIES.get(key, 0)
            + THREE_GRAM_ITP_WEIGHT * THREE_GRAM_PROBABILITIES.get(key, 0)
            + TWO_GRAM_ITP_WEIGHT * TWO_GRAM_PROBABILITIES.get(key, 0)
        )

    return next_word_probabilities


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
    punct_spacing = " "

    context_string = " ".join(current_context_list)
    probabilities = interpolated_probability(context_string)
    smaller_sorted_probabilities = apply_p_word_sampling(probabilities, P_WORD_LIMIT)

    if not smaller_sorted_probabilities:
        print("No data found. Try a different phrase.")
        break
    else:
        sampled_num = random.random()
        next_word, next_word_index, curr_range, new_context_list = generate_next_word(smaller_sorted_probabilities, sampled_num, current_context_list)
        if next_word in string.punctuation:
            punct_spacing = ""
        print(punct_spacing + next_word, end="", flush=True)        
        time.sleep(0.125)
        generated_sentence_list.append(next_word)
        current_context_list = new_context_list

        if next_word == ".":
            has_period = True

# sentence = " ".join(generated_sentence_list)
# sentence = re.sub(r"\s+([,.])", r"\1", sentence)
# print(sentence)
