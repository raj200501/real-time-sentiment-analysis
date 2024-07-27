import requests
import json
import time
from kafka import KafkaProducer

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to fetch news articles
def fetch_news():
    url = ('http://newsapi.org/v2/everything?'
           'q=Snowflake&'
           'apiKey=your_newsapi_key')
    response = requests.get(url)
    return response.json()

# Sending news articles to Kafka topic
while True:
    news_data = fetch_news()
    for article in news_data['articles']:
        news = {
            'title': article['title'],
            'description': article['description'],
            'published_at': article['publishedAt']
        }
        print(f"Sending news: {news}")
        producer.send('news_topic', value=news)
    time.sleep(300)  # Fetch news every 5 minutes
