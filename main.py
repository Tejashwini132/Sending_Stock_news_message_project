import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "ICR3VSV38C3DR8RG"
NEWS_API_KEY = "ea7b33656ce940b59955ad8fe8f3974a"
account_sid = "AC9b1c5eb4acd340b0bb26684e7b65b92f"  # https://console.twilio.com/?frameUrl=%2Fconsole%3Fx-target-region%3Dus1
auth_token = "852dd05d700513011f1fc2eefb253fc2"  # get from above link

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

# yesterday's closing stock price.list comprehensions on Python dictionaries.
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)
# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)
# Find the positive difference between 1 and 2.
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
print(difference)
up_down = None
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"
# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)
# If TODO4 percentage is greater than 5 then print("Get News").
if abs(diff_percent) > 5:

    # Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]

    # Use Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]
    # to send a separate message with each article's title and description to your phone number.

    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_article = [f"{STOCK_NAME}:{up_down}{diff_percent}%\nHeadlines:{article['title']}\n "\
                         f"Brief:{article['description']}" for article in three_articles]
    # Send each article as a separate message via Twilio.
    client = Client(account_sid, auth_token)
    for article in formatted_article:
        message = client.messages \
            .create(
            body=article,
            from_="+19282720977",
            to="+917022120036"
        )
        print(message.status)
