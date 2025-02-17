from kafka import KafkaProducer
import yfinance as yf
import json
import time

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "stock_prices"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# List of stock tickers to track
stock_tickers = ["AAPL", "GOOG", "MSFT", "AMZN"]

def fetch_stock_data():
    """Fetch latest stock market data from Yahoo Finance"""
    stock_data = {}
    for ticker in stock_tickers:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")
        if not history.empty:
            stock_info = history.iloc[-1]
            stock_data[ticker] = {
                "timestamp": time.time(),
                "open": stock_info["Open"],
                "high": stock_info["High"],
                "low": stock_info["Low"],
                "close": stock_info["Close"],
                "volume": int(stock_info["Volume"])
            }
    return stock_data

if __name__ == "__main__":
    while True:
        data = fetch_stock_data()
        if data:
            print(f"Sending stock data: {data}")
            producer.send(KAFKA_TOPIC, data)
        time.sleep(5)  # Send new stock data every 5 seconds
