import json
from confluent_kafka import Consumer, KafkaException

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
            
            # Poll for new messages
            message = consumer.poll(timeout = 1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaException._PARTITION_EOF:
                    # End of partition event
                    print('%% %s [%d] reached end at offset %d\n' %
                          (message.topic(), message.partition(), 
                           message.offset()))
                elif message.error():
                    raise KafkaException(message.error())
            else:
                # Process the message
                print('Received message: {}'.format(message.value().decode('utf-8')))
                
    finally:
        # Close the consumer
        consumer.close()
        
# Start consuming messages
process_messages()

