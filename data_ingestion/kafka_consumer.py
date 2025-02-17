from kafka import KafkaConsumer
import json
import psycopg2

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "stock_prices"

# Connect to PostgreSQL (simulate Redshift/PostgreSQL locally)
conn = psycopg2.connect(
    dbname="finance_db",
    user="your_user",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_data (
        ticker TEXT,
        timestamp BIGINT,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume INT
    );
""")
conn.commit()

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Listening for stock data...")

for message in consumer:
    stock_data = message.value
    for ticker, data in stock_data.items():
        cursor.execute("""
            INSERT INTO stock_data (ticker, timestamp, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (ticker, data["timestamp"], data["open"], data["high"], data["low"], data["close"], data["volume"]))
    conn.commit()
    print(f"Stored data: {stock_data}")
