from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from transformers import pipeline

app = Flask(__name__)

# Load the stock price forecasting model
stock_model = tf.keras.models.load_model("ai_models/stock_price_model.h5")
# Load local NLP model for sentiment analysis
nlp_model = pipeline("sentiment-analysis")

@app.route("/predict_stock", methods=["POST"])
def predict_stock():
    """
    Expects JSON with a key "prices" containing a list of past 'close' prices.
    """
    data = request.json.get("prices")
    if not data:
        return jsonify({"error": "No data provided"}), 400
    # Reshape data for LSTM prediction
    data = np.array(data).reshape(1, -1, 1)
    prediction = stock_model.predict(data)
    return jsonify({"predicted_price": float(prediction[0][0])})

@app.route("/analyze_sentiment", methods=["POST"])
def analyze_sentiment():
    """
    Expects JSON with a key "text" containing the text to analyze.
    """
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    sentiment = nlp_model(text)
    return jsonify(sentiment)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
