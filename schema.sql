DROP TABLE IF EXISTS ngrams;

CREATE TABLE ngrams (
    n_length INTEGER NOT NULL,
    context TEXT NOT NULL,
    next_word TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (n_length, context, next_word)
);