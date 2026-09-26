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
    # Austen, Bronte, Shelley & Early 19th Century
    1342, 158, 161, 141, 121, 105, 84, 1260, 768, 969, 
    # Dickens & Victorian Fiction
    98, 1400, 46, 730, 766, 1023, 580, 514, 550, 145, 1250, 675, 4363, 16, 11, 12,
    # Twain, Melville & American Classics
    76, 74, 86, 1837, 2701, 205, 33, 215, 30, 209, 100, 3207,
    # Doyle (Sherlock Holmes) & Detective/Mystery
    1661, 2852, 244, 834, 2097, 345, 174,
    # Adventure & Classic Fiction
    120, 43, 1184, 219, 829, 996, 55, 42, 132, 140, 2148, 236, 2856, 3296, 3600,
    # H.G. Wells, Sci-Fi & Speculative Fiction
    36, 35, 5230, 4085, 4140, 513, 6130, 64317, 7370,
    # Russian Classics (English Translations)
    2600, 1399, 28054, 600, 135, 2591, 1952,
    # Philosophy, Drama & World Classics (English Translations)
    5200, 4300, 1727, 1232, 45, 2413, 160, 2814, 30254, 20203,
    # Additional High-Token Literary Works
    767, 851, 883, 910, 1155, 1257, 1377, 1597, 1600,
    1656, 1664, 1719, 1726, 1787, 1826, 1858, 1877, 1900, 1905, 1928, 1934, 1946,
    1951, 1998, 2005, 2009, 2015, 2020, 2041, 2060, 2077, 2084, 2099, 2101,
    2111, 2112, 2114, 2118, 2120, 2125, 2130, 2135, 2140, 2145, 2150, 2155, 2160,
    2165, 2170, 2180, 2185, 2225
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
