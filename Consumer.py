import json
from confluent_kafka import Consumer, KafkaError

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'stock_data_group',
    'auto.offset.reset': 'earliest'    
}

# Initialize consumer
consumer = Consumer(**conf)
consumer.subscribe(['stock_prices'])

# Function to consume and process stock data
def process_messages():
    try:
        while True:
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print('%% %s [%d] reached end at offset %d\n' %
                          (message.topic(), message.partition(), 
                           message.offset()))
                elif message.error():
                    print('Error: {}'.format(message.error()))
                    raise KafkaError(message.error())
            else:
                # No error, process the message
                print('Received message: {}'.format(message.value().decode('utf-8')))
                
    finally:
        # Close the consumer
        consumer.close()
        
# Start consuming messages
process_messages()


