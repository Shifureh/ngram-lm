DROP TABLE IF EXISTS ngrams;

CREATE TABLE ngrams (
    n_length INTEGER,
    context TEXT,
    next_word TEXT,
    count INTEGER
);