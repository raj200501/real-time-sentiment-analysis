-- SQLite schema used by the local sentiment analysis pipeline.

CREATE TABLE IF NOT EXISTS sentiment_records (
    record_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    sentiment TEXT NOT NULL,
    polarity REAL NOT NULL,
    raw_payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sentiment_source ON sentiment_records(source);
CREATE INDEX IF NOT EXISTS idx_sentiment_label ON sentiment_records(sentiment);
