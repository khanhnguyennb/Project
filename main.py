
import requests
from twilio.rest import Client

STOCK_NAME = "AAPL"
COMPANY_NAME = "Apple Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "XPR9DE3QEDHWMJE7"
NEWS_API_KEY = "62099415a9f441edbb73058696c4acfb"
TWILIO_SID = "ACf29cd982deb6388eb56ee759ef538dde"
TWILIO_AUTH_TOKEN = "4cbe26c029bb1851c3f44206da45f287"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data_list = (response.json()["Time Series (Daily)"])
data = []
for (key, value) in data_list.items():
    data.append(value)

yesterday_data = data[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

price_difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
fluctuation = None
if price_difference > 5:
    fluctuation = "📈"
else:
    fluctuation = "📉"

percent_change = round((price_difference/float(yesterday_closing_price))*100)

if abs(percent_change) > 0:
    news_params = {
        "apiKey": "62099415a9f441edbb73058696c4acfb",
        "q": COMPANY_NAME and STOCK_NAME,
        "qInContent": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    # print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {fluctuation} {abs(percent_change)}%\n\nHeadline: {article['title']}.\n\nBrief: {article['description']}" for article in three_articles]

    print(formatted_articles)

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        notification = client.messages.create(
            body=article,
            from_="=+18559564034",
            to="+18135858900"
        )

















