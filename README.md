# Real-time Sentiment Analysis and Data Integration Platform

## Project Overview
This project provides a deterministic, local simulation of a real-time sentiment analysis pipeline. It ingests sample Twitter/news data from JSONL files, performs sentiment analysis using a curated lexicon, and stores the enriched records in a SQLite database for analytics.

The repository is self-contained: no external APIs, Kafka brokers, or Snowflake accounts are required. Every command described here is reproducible in a clean checkout.

## Repository Structure
- `data_ingestion`: Compatibility wrappers for ingesting sample data.
- `sentiment_analysis`: Compatibility wrapper to run the pipeline.
- `snowflake_integration`: Local SQLite schema and compatibility wrapper for data loading.
- `analytics`: SQL queries for analyzing the data stored in SQLite.
- `src/sentiment_platform`: Core pipeline implementation.
- `data`: Sample JSONL data used for deterministic ingestion.
- `scripts`: Canonical run and verification scripts.

## README Contract
### Install
```bash
python -m pip install -r requirements.txt
```

### Configure
Optional `.env` overrides are supported. Start from the template:
```bash
cp .env.example .env
```

### Run
Run the pipeline with sensible defaults:
```bash
./scripts/run.sh
```

Expected behavior:
- A SQLite database is created at `./var/sentiment.db`.
- The pipeline ingests the sample data in `data/`, analyzes sentiment, and persists the results.
- A summary of inserted records and sentiment counts is printed.

### Verify/Test
Run the canonical verification command:
```bash
./scripts/verify.sh
```

The verification command:
- Runs unit tests (Python `unittest`)
- Executes an end-to-end smoke test that ingests data, analyzes sentiment, and validates the SQLite output

## Verified Quickstart (Executed)
```bash
python -m pip install -r requirements.txt
./scripts/run.sh
```

## Verified Verification (Executed)
```bash
./scripts/verify.sh
```

## Usage Details
### 1. Ingest Sample Data
```bash
python data_ingestion/twitter_ingestion.py
python data_ingestion/news_ingestion.py
```

### 2. Run Sentiment Analysis Pipeline
```bash
python sentiment_analysis/sentiment_analysis.py
```

### 3. Load Data (SQLite)
```bash
python snowflake_integration/load_to_snowflake.py
```

### 4. Analytics
Use the SQL queries in `analytics/analytics_queries.sql` with SQLite:
```bash
sqlite3 ./var/sentiment.db < analytics/analytics_queries.sql
```

## Configuration Reference
- `DATABASE_PATH`: Path to the SQLite database (default: `./var/sentiment.db`).
- `TWITTER_SOURCE_PATH`: JSONL file with sample Twitter data.
- `NEWS_SOURCE_PATH`: JSONL file with sample news data.
- `OUTPUT_DIR`: Directory for pipeline artifacts.
- `MAX_RECORDS_PER_SOURCE`: Optional per-source limit on ingested records.

## Troubleshooting
- **Missing dependencies**: run `python -m pip install -r requirements.txt` (no external packages required).
- **SQLite output missing**: ensure `./scripts/run.sh` is executed from the repo root.
- **Custom data**: replace the JSONL files in `data/` but preserve the required keys:
  - Twitter: `id`, `text`, `created_at`
  - News: `id`, `description`, `published_at`

## Conclusion
The platform now offers a repeatable, local workflow for ingestion, sentiment analysis, and analytics without requiring external services. The scripts and tests provide automated proof that the pipeline behaves as described.
