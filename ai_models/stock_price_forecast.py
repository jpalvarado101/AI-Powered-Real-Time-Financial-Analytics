import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Load historical stock data (CSV exported from database or ETL)
df = pd.read_csv("data/stock_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df.sort_values("timestamp", inplace=True)
df.reset_index(drop=True, inplace=True)

# Use the 'close' column for forecasting
data = df["close"].values.reshape(-1, 1)

# Scale data between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data)

# Create training data
sequence_length = 60
X_train, y_train = [], []
for i in range(sequence_length, len(data_scaled)):
    X_train.append(data_scaled[i-sequence_length:i, 0])
    y_train.append(data_scaled[i, 0])
    
X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Build the LSTM model
model = Sequential([
    LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    LSTM(units=50, return_sequences=False),
    Dense(units=25),
    Dense(units=1)
])

model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(X_train, y_train, epochs=10, batch_size=16)

# Save the model
model.save("ai_models/stock_price_model.h5")
print("LSTM model trained and saved!")
