import tweepy
import json
import time
from kafka import KafkaProducer

# Twitter API credentials
API_KEY = 'your_api_key'
API_SECRET_KEY = 'your_api_secret_key'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Tweepy authentication
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# StreamListener class to get live tweets
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet = {
            'text': status.text,
            'created_at': status.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"Sending tweet: {tweet}")
        producer.send('twitter_topic', value=tweet)

    def on_error(self, status_code):
        if status_code == 420:
            return False

# Start streaming tweets
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['Snowflake'])

# Add a sleep to prevent too many requests in a short period
time.sleep(60)
