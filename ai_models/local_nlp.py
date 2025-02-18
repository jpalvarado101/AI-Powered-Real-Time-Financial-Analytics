from transformers import pipeline

# Load sentiment analysis model locally
nlp_model = pipeline("sentiment-analysis")

# Sample text for testing
sample_text = "The stock market is experiencing a significant downturn."

result = nlp_model(sample_text)
print("Sentiment Analysis Result:", result)
