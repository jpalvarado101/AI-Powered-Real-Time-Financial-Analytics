import requests
import json

# Example using NewsAPI (replace YOUR_API_KEY with an actual key)
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "YOUR_API_KEY"

def fetch_news():
    params = {
        "category": "business",
        "apiKey": API_KEY,
        "country": "us"
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        news_data = response.json()
        return news_data
    else:
        return {}

if __name__ == "__main__":
    news = fetch_news()
    print(json.dumps(news, indent=2))
