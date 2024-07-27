# Real-time Sentiment Analysis and Data Integration Platform

## Project Overview
This project demonstrates a real-time sentiment analysis and data integration platform using Kafka, Python, and Snowflake. The platform ingests data from Twitter and news sources, performs sentiment analysis using TextBlob, and stores the results in Snowflake for further analysis.

## Repository Structure
- `data_ingestion`: Scripts for ingesting data from Twitter and news sources.
- `sentiment_analysis`: Script for performing sentiment analysis on the ingested data.
- `snowflake_integration`: Scripts for setting up Snowflake and loading data into Snowflake.
- `analytics`: SQL queries for analyzing the data stored in Snowflake.

## Setup Instructions

### 1. Kafka Setup
- Install Kafka and start the Kafka server.
- Create Kafka topics: `twitter_topic`, `news_topic`, `sentiment_topic`.

### 2. Python Dependencies
Install the required Python packages using pip:
```bash
pip install tweepy kafka-python textblob requests snowflake-connector-python
```
## 3. Run Data Ingestion Scripts
```bash
python data_ingestion/twitter_ingestion.py
python data_ingestion/news_ingestion.py
```
## 4. Run Sentiment Analysis Script
```bash
python sentiment_analysis/sentiment_analysis.py
```
## 5. Setup Snowflake
Run the SQL script to setup Snowflake:
```bash
snowflake_integration/setup_snowflake.sql
```
## 6. Run Data Loading Script
```bash
python snowflake_integration/load_to_snowflake.py
```
## 7. Analytics
Use the SQL queries in analytics/analytics_queries.sql to analyze the data in Snowflake.

# Conclusion
This project showcases the integration of various technologies to build a real-time data analytics platform. It demonstrates how to ingest, process, and analyze data in real-time, providing valuable insights through sentiment analysis.

