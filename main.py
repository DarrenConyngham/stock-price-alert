import config
import requests
from datetime import datetime, timedelta
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# getting the data
params = {'function': 'TIME_SERIES_DAILY',
          'symbol': STOCK,
          'outputsize': 'compact',
          'apikey': config.ALPHA_VANTAGE_API_KEY}

url = 'https://www.alphavantage.co/query?'
r = requests.get(url, params=params)
data = r.json()


# processing the data
def prev_weekday(adate):
    adate -= timedelta(days=1)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate


current_date = datetime.today()
yesterday_date = prev_weekday(current_date)
day_before_yesterday_date = prev_weekday(yesterday_date)
yesterday_date = yesterday_date.strftime('%Y-%m-%d')
day_before_yesterday_date = day_before_yesterday_date.strftime('%Y-%m-%d')

yesterday_close = float(data["Time Series (Daily)"]
                        [yesterday_date]['4. close'])
day_before_yesterday_close = float(
    data["Time Series (Daily)"][day_before_yesterday_date]['4. close'])


def get_perc_change(final_value, initial_value):
    """Calculates the percentage change between two values.

    Args:
        final_value (float): the later value you wish to input.
        initial_value (float): the earlier value you wish to input.

    Returns:
        float: the percentage change in the decimal format (e.g. 0.04 and not 4%)
    """    
    perc_change = (final_value - initial_value) / initial_value
    return perc_change


perc_change_res = get_perc_change(yesterday_close, day_before_yesterday_close)


# fetching and sending news data
if abs(perc_change_res) > 0.05:
    params = {"q": COMPANY_NAME,
              "searchIn": "title,description",
              "from": yesterday_date,
              "sortBy": 'popularity',
              "apiKey": config.NEWS_API_KEY}

    url = 'https://newsapi.org/v2/everything?'

    r = requests.get(url, params=params)
    data = r.json()

    top_three_articles = data["articles"][:3]

    for i in range(3):
        selected_article = top_three_articles[i]
        print("Fetched article")
        client = Client(config.twilio_account_sid, config.twilio_auth_token)
        message = client.messages.create(
            body=f"{STOCK} daily change: {round(perc_change_res*100, 2)}%\nHeadline: {selected_article['title']}\nBrief: {selected_article['description']}",
            from_=config.twilio_phone_num,
            to=config.my_phone_num)
        print(message.status)
