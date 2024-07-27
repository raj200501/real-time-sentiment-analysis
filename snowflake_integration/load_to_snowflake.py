import json
from kafka import KafkaConsumer
import snowflake.connector

# Kafka consumer configuration
consumer = KafkaConsumer(
    'sentiment_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Snowflake connection configuration
conn = snowflake.connector.connect(
    user='your_username',
    password='your_password',
    account='your_account',
    warehouse='your_warehouse',
    database='sentiment_analysis_db',
    schema='public'
)

cur = conn.cursor()

# Consuming messages and loading data into Snowflake
for message in consumer:
    data = message.value
    cur.execute(
        f"""
        INSERT INTO sentiment_data (text, created_at, sentiment, source)
        VALUES ('{data.get('text', '')}', '{data.get('created_at')}', '{data.get('sentiment')}', 'Twitter' if 'text' in data else 'News')
        """
    )
    conn.commit()
    print("Data inserted into Snowflake")
