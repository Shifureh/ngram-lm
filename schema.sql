CREATE TABLE IF NOT EXISTS ngrams (
    context TEXT NOT NULL,
    next_word TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (context, next_word) 
);