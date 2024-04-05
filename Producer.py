
# Libraries
import json
import time
import yfinance as yf
from confluent_kafka import Producer

# Kafka configuration

conf = {
    'bootstrap.servers': 'localhost:9092',
}

# Initialize producer
producer = Producer(**conf)

# Function to fetch and publish stock data
def fetch_and_publish_stock_data(stock_symbol):
    while True:
        # Fetch stock data from Yahoo Finance
        stock_data = yf.Ticker(stock_symbol)
        stock_history = stock_data.history(period="1m")  # Fetching 1-minute interval data

        if not stock_history.empty:
            # Get the latest record from the DataFrame
            latest_record = stock_history.iloc[-1]
            
            # Prepare the message
            message = {
                'symbol': stock_symbol,
                'price': latest_record['Close'],
                'date': str(stock_history.index[-1].to_pydatetime())  # Convert the timestamp to a readable format
            }

            # Publish to Kafka topic
            producer.produce('stock_prices', key=stock_symbol, value=json.dumps(message))
            producer.flush()

        # Sleep for a minute before fetching the next update
        time.sleep(60)

# Example usage
fetch_and_publish_stock_data('AAPL')
        