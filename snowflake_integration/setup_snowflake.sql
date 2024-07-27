-- setup_snowflake.sql

-- Create database
CREATE DATABASE IF NOT EXISTS sentiment_analysis_db;

-- Use the created database
USE DATABASE sentiment_analysis_db;

-- Create schema
CREATE SCHEMA IF NOT EXISTS public;

-- Use the created schema
USE SCHEMA public;

-- Create table to store sentiment data
CREATE TABLE IF NOT EXISTS sentiment_data (
    id INTEGER AUTOINCREMENT,
    text STRING,
    created_at TIMESTAMP,
    sentiment STRING,
    source STRING
);
