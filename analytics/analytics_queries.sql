-- analytics_queries.sql (SQLite)

-- Query to get the count of positive/negative/neutral sentiments
SELECT sentiment, COUNT(*) AS count
FROM sentiment_records
GROUP BY sentiment
ORDER BY sentiment;

-- Query to get the sentiment trend over time
SELECT date(created_at) AS date, sentiment, COUNT(*) AS count
FROM sentiment_records
GROUP BY date, sentiment
ORDER BY date, sentiment;

-- Query to get the latest five records
SELECT record_id, source, sentiment, created_at
FROM sentiment_records
ORDER BY datetime(created_at) DESC
LIMIT 5;
