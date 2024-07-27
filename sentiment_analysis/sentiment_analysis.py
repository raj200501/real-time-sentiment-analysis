import json
from kafka import KafkaConsumer, KafkaProducer
from textblob import TextBlob

# Kafka consumer configuration
consumer = KafkaConsumer(
    'twitter_topic',
    'news_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return 'positive' if analysis.sentiment.polarity > 0 else 'negative'

# Consuming messages and analyzing sentiment
for message in consumer:
    data = message.value
    data['sentiment'] = analyze_sentiment(data.get('text', '') or data.get('description', ''))
    print(f"Analyzed data: {data}")
    producer.send('sentiment_topic', value=data)
