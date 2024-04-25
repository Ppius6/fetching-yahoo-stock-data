# Real-Time Stock Data Visualization

This project demonstrates how to fetch real-time stock data using Yahoo Finance, publish it to a Kafka topic, and visualize it using a Dash application. The system architecture includes a Kafka producer (fetching data from Yahoo Finance), a Kafka consumer (subscribed to the Kafka topic), and a Dash app for real-time visualization.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- Apache Kafka
- Confluent Kafka Python client library
- Flask
- Dash and Dash Bootstrap Components
- Pandas
- Plotly
- Yahoo Finance API (yfinance)

## Setup Instructions

### Kafka Setup

1. **Start Zookeeper**:
   ```bash
   zookeeper-server-start.sh config/zookeeper.properties
   ```

2. **Start Kafka Server**:
    ```bash
    kafka-server-start.sh config/server.properties
    ```

For the application setup:

1. Clone the repository
    ```
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Create a virtual environment
    ```
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install the dependencies listed before.

4. Configure Kafka: Ensure that Kafka is configured in `producer.py` and c`onsumer.py` scripts:
    ```
    kafka_conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'stock_data_group',
        'auto.offset.reset': 'earliest'
    }
    ```
5. Run the Producer: Start the Kafka producer to fetch data from Yahoo Finance and publish it to a Kafka topic
    ```
    python producer.py
    ```

6. Run the Consumer: Start the Kafka consumer to consume data from the Kafka topic:
    ```
    python consumer.py
    ```

7. Start the Dash Application:
    ```
    python app.py
    ```

## Usage
Once all components are up and running, navigate to http://127.0.0.1:8050/ in your web browser to view the real-time stock data visualization. The graph updates every second to reflect the latest stock prices fetched from Yahoo Finance.

## Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.
