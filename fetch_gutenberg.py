import requests
import os

def strip_gutenberg_boilerplate(text):
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start = text.find(start_marker)
    end = text.find(end_marker)

    if start != -1:
        start = text.find("\n", start) + 1
    else:
        start = 0

    if end == -1:
        end = len(text)

    return text[start:end].strip()


BOOK_IDS = [
    1342, 158, 161, 141,           # Austen: Pride and Prejudice, Emma, Sense and Sensibility, Mansfield Park
    11, 12,                        # Carroll: Alice's Adventures in Wonderland, Through the Looking-Glass
    84,                            # Shelley: Frankenstein
    76, 74, 86,                    # Twain: Huck Finn, Tom Sawyer, A Connecticut Yankee
    2701,                          # Melville: Moby-Dick
    345,                           # Stoker: Dracula
    174, 844,                      # Wilde: The Picture of Dorian Gray, The Importance of Being Earnest
    98, 1400, 46, 730,             # Dickens: Tale of Two Cities, Great Expectations, A Christmas Carol, Oliver Twist
    36, 35,                        # Wells: War of the Worlds, The Time Machine
    514,                           # Alcott: Little Women
    1260, 768,                     # Brontë: Jane Eyre, Wuthering Heights
    1661, 2852, 244,               # Doyle: Sherlock Holmes, Hound of the Baskervilles, A Study in Scarlet
    1184,                          # Dumas: The Count of Monte Cristo
    135,                           # Hugo: Les Misérables
    2600, 1399,                    # Tolstoy: War and Peace, Anna Karenina
    55,                            # Baum: The Wonderful Wizard of Oz
    120, 43,                       # Stevenson: Treasure Island, Dr. Jekyll and Mr. Hyde
    219,                           # Conrad: Heart of Darkness
    205,                           # Thoreau: Walden
    829,                           # Swift: Gulliver's Travels
    5200,                          # Kafka: Metamorphosis
    996,                           # Cervantes: Don Quixote
    33,                            # Hawthorne: The Scarlet Letter
    550,                           # Eliot: Silas Marner
    145,                           # Eliot: Middlemarch
    4300,                          # Joyce: Ulysses
    1727,                          # Homer: The Odyssey (Butler translation)
]

def fetch_all_books(book_ids=BOOK_IDS, data_folder="data"):
    os.makedirs(data_folder, exist_ok=True)

    for book_id in book_ids:
        filepath = f"{data_folder}/{book_id}.txt"

        if os.path.exists(filepath):
            print(f"{book_id} already exists, skipping download")
            continue

        response = requests.get(
            f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
            timeout=10
        )
        print(book_id, response.status_code)

        clean_text = strip_gutenberg_boilerplate(response.text)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(clean_text)

        print(f"Saved {len(clean_text)} characters to {filepath}")


if __name__ == "__main__":
    fetch_all_books()