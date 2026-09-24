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
- `preprocess_text.py` — tokenizes text (words + punctuation, contraction-aware, normalizes curly apostrophes)
- `build_ngrams.py` — orchestrates fetch → preprocess → builds n=2 through 4-gram counts into SQLite
- `generate.py` — generates text using interpolated smoothing across n-gram orders (blends weighted probabilities from 4-gram, trigram, and bigram simultaneously, weights: 0.70/0.20/0.10), with top-p (nucleus) sampling to filter low-probability candidates before random selection
- `schema.sql` — database schema (n_length, context, next_word, count)

## Corpus
40 public-domain novels from Project Gutenberg, spanning Austen, Dickens, Twain, Doyle, Tolstoy, and others — see `fetch_gutenberg.py` for the full list.

## Findings
Average n-gram count across the final 40-book corpus:

| n | unique contexts | average count |
|---|---|---|
| 2 | 1,234,307 | 5.91 |
| 3 | 3,848,332 | 1.90 |
| 4 | 6,004,332 | 1.22 |

Even at this corpus scale, 4-gram contexts remain dominated by singleton occurrences (avg. count 1.22), demonstrating a core limitation of n-gram models regardless of data volume. This is what motivates the use of a neural model approach seen below.

## Sample Generations
Seed: `"it is a"` — 8 runs, no cherry-picking:
- it is a clever fellow, my sister, and solomon your own doing.
- it is a good fellow, if you wanted to read it aloud to me.
- it is a wine stain, fruit hung golden in the orchard were ungrafted, and wild flowers in the home farm go there at a venture, keeping in shadow, and am the more tranquil and terrible continuity.
- it is a curly haired spaniel.
- it is a good knight.
- it is a strange change approaching i'm in love with you.
- it is a perfect cyclops, isn't she asked laurie anxiously.
- it is a curious thing that she is the very question i do not a horrible caprice to me.

Output shows real variety (no repeated outputs across runs) and generally sound local grammar, but longer generations reveal the model's lack of long-range coherence — a direct illustration of the n-gram limitation above.

## Known Limitations
- Table-of-contents sections in some source texts introduce minor structural noise (roman numerals, title fragments) into n-gram counts; left unaddressed given the small proportion of overall text affected.
- Interpolation weights (0.70/0.20/0.10) are fixed manually rather than tuned empirically against held-out data.

## Neural Model (in progress)
Comparison of n-gram vs. neural next-word prediction — coming soon.

## Team
- Shifatul Gani — data pipeline, database schema, generation logic (interpolation, sampling)
- Arabi Sayed — generation logic (probability & word generation, top-p (nucleus) sampling), program optimization
- Tahseen Ullah — data pipeline, database schema, data querying, program optimization