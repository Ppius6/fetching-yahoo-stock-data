from flask import Flask, render_template, jsonify
from confluent_kafka import Consumer, KafkaException
import json
import threading

# Initialize Flask app
app = Flask(__name__)

# Kafka configuration
kafka_conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'stock_data_group',
        'auto.offset.reset': 'earliest'
    }

# Variables to store stock data
latest_stock_data = {}

# Function to consume kafka messages
def consume_messages():
    consumer = Consumer(**kafka_conf)
    consumer.subscribe(['stock_prices'])
    
    try:
        while True:
            message = consumer.poll(timeout = 1.0)
            if message is None:
                continue
            if message.error() and message.error().code() != KafkaException._PARTITION_EOF:
                raise KafkaException(message.error())
            else:
                stock_data = json.loads(message.value().decode('utf-8'))
                symbol = stock_data['symbol']
                if symbol not in latest_stock_data:
                    latest_stock_data[symbol] = []
                latest_stock_data[symbol].append(stock_data)
    finally:
        consumer.close()
        
# Thread to run the Kafka consumer
threading.Thread(target = consume_messages, daemon = True).start()

@app.route('/')
def index():
    return render_template('index.html', stock_data = latest_stock_data)

@app.route('/stock-data')
def stock_data():
    return jsonify(latest_stock_data)

if __name__ == '__main__':
    app.run(debug = True)