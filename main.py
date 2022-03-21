import config
import requests
from datetime import datetime, timedelta


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

### getting the data
params = {'function': 'TIME_SERIES_DAILY',
            'symbol': STOCK,
            'outputsize': 'compact',
            'apikey': config.ALPHA_VANTAGE_API_KEY}

url = 'https://www.alphavantage.co/query?'
r = requests.get(url, params=params)
data = r.json()


### processing the data
def prev_weekday(adate):
    adate -= timedelta(days=1)
    while adate.weekday() > 4: # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate

current_date = datetime.today()

yesterday_date = prev_weekday(current_date)
day_before_yesterday_date = prev_weekday(yesterday_date)
yesterday_date = yesterday_date.strftime('%Y-%m-%d')
day_before_yesterday_date = day_before_yesterday_date.strftime('%Y-%m-%d')

yesterday_close = float(data["Time Series (Daily)"][yesterday_date]['4. close'])
day_before_yesterday_close = float(data["Time Series (Daily)"][day_before_yesterday_date]['4. close'])

def is_change_greater_than_perc(final_value, initial_value, percentage=0.01):
    perc_change = abs((final_value - initial_value) / initial_value)
    print(f"The initial close was: {initial_value}. The final close was: {final_value}. The absolute perc change was: {perc_change}")
    if perc_change > percentage:
        print("Get News")
        return True
    return False

res = is_change_greater_than_perc(yesterday_close, day_before_yesterday_close)
print(res)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

