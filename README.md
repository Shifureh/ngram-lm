# ngram-lm
N-gram and neural language model trained on Project Gutenberg text — built from scratch in Python and SQLite. Demonstrates classical n-gram statistics, their sparsity limitations, and how a neural approach improves generalization.

## Setup
git clone <repo-url>
cd ngram-lm
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python build_ngrams.py    # fetches all 40 books + builds n-gram database (first run takes a while)
python generate.py        # generates text from the trained model

## Structure
- `fetch_gutenberg.py` — downloads and cleans 40 Project Gutenberg texts (called automatically by build_ngrams.py)
- `preprocess_text.py` — tokenizes text (words + punctuation, contraction-aware)
- `build_ngrams.py` — orchestrates fetch → preprocess → builds n=2 through 4-gram counts into SQLite
- `generate.py` — generates text using backoff across n-gram orders (tries 4-gram, falls back to trigram/bigram)
- `schema.sql` — database schema (n_length, context, next_word, count)

## Corpus
40 public-domain novels from Project Gutenberg, spanning Austen, Dickens, Twain, Doyle, Tolstoy, and others — see `fetch_gutenberg.py` for the full list.

## Known Limitations
- Table-of-contents sections in some source texts introduce minor structural noise (roman numerals, title fragments) into n-gram counts; left unaddressed given the small proportion of overall text affected.
- Generation uses backoff (highest available n-gram order, falling back when data is sparse) but does not yet implement full interpolation smoothing.

## Neural Model (in progress)
Comparison of n-gram vs. neural next-word prediction — coming soon.

## Team
- Shifatul Gani
- Arabi Sayed
- Tahseen Ullah