-- analytics_queries.sql

-- Use the database and schema
USE DATABASE sentiment_analysis_db;
USE SCHEMA public;

-- Query to get the count of positive and negative sentiments
SELECT sentiment, COUNT(*) AS count
FROM sentiment_data
GROUP BY sentiment;

-- Query to get the sentiment trend over time
SELECT created_at::date AS date, sentiment, COUNT(*) AS count
FROM sentiment_data
GROUP BY date, sentiment
ORDER BY date;
