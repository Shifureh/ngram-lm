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


response = requests.get("https://gutendex.com/books", params={"search": "sherlock holmes"})
books = response.json()["results"]


BOOK_IDS = [100]

os.makedirs("data", exist_ok=True)

for book_id in BOOK_IDS:
    response = requests.get(
    f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
    timeout=10
    )
    print(book_id, response.status_code)

    clean_text = strip_gutenberg_boilerplate(response.text)

    with open(f"data/{book_id}.txt", "w", encoding="utf-8") as f:
        f.write(clean_text)

    print(f"Saved {len(clean_text)} characters to data/{book_id}.txt")