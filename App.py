import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import pandas as pd
import threading
from flask import Flask
from confluent_kafka import Consumer, KafkaError
import json
from collections import defaultdict
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)

dash_app = dash.Dash(__name__, server = app, external_stylesheets = [dbc.themes.BOOTSTRAP])

kafka_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'stock_data_group',
    'auto.offset.reset': 'earliest'
}

latest_stock_data = {}

lock = threading.Lock()

# Initialize a dictionary to hold lists of data points for each stock symbol
stock_data_history = defaultdict(list)

def consume_messages():
    consumer = Consumer(**kafka_conf)
    consumer.subscribe(['stock_prices'])
    
    try:
        while True:
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                print("Kafka error:", message.error())
            else:
                stock_data = json.loads(message.value().decode('utf-8'))
                with lock:
                    # Append each new data point to the list for the given stock symbol
                    stock_data_history[stock_data['symbol']].append(stock_data)
    finally:
        consumer.close()

consumer_thread = threading.Thread(target = consume_messages, daemon = True)

consumer_thread.start()

dash_app.layout = html.Div([
    html.H1('Real-Time Stock Data', style = {'textAlign': 'center'}),
    dcc.Graph(id = 'stock-graph'),
    dcc.Interval(id = 'interval-component', interval = 1*1000, n_intervals = 0)  # Updates every second
])


@dash_app.callback(
    Output('stock-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)

def update_graph(n):
    
    bars = []
    
    with lock:
        # Prepare a list of the latest stock prices
        latest_prices = [{'symbol': symbol, 'price': data[-1]['price']} for symbol, data in stock_data_history.items() if data]
        df = pd.DataFrame(latest_prices)
    
    if not df.empty:
        bars = [go.Bar(
            x=df['symbol'],  # Stock symbols as x
            y=df['price'],  # Stock prices as y
            marker=dict(color=df['price'], coloraxis="coloraxis")  # Colors can represent prices
        )]

    figure = go.Figure(data=bars)
    figure.update_layout(
        title='Latest Stock Prices',
        xaxis=dict(title='Stock'),
        yaxis=dict(title='Price ($)'),
        coloraxis=dict(colorscale='Viridis'),  # Using a colorscale for bar colors
        showlegend=False  # No legend necessary for a bar chart
    )
    
    return figure

if __name__ == '__main__':
    app.run(debug=True)
