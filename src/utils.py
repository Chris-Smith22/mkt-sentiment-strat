# utils.py - contains functions necessary to run main.py
import sys  
import os                   #to import authentification
import datetime as dt
import pandas as pd
import re                   #regex

## Data Analysis APIs:
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import yfinance as yf

## Web Scrapers:
import requests         
from bs4 import BeautifulSoup as bs     #web scraper

## Reddit API access
import praw   
from auth import *          #authentification details - create an auth.py file in code/ with authentification details
import prawcore

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT)

date_format = "%Y-%m-%d"

# FUNCTIONS:

## Sentiment Functions:
def postSentiment(urlT):
    try:
        post = reddit.submission(url=urlT)
        pbody = post.selftext
        #print(post.title)
    except:
        return 0
    

    sia = SIA()
    body_sentiments = sia.polarity_scores(pbody)
    
    title_sentiment = sia.polarity_scores(post.title)

    avg_sentiment = (body_sentiments['compound']+title_sentiment['compound'])/2
    
    '''print(avg_sentiment)
    
    for key in title_sentiment.keys():
        print(key, title_sentiment[key])
    
    for key in body_sentiments.keys():
        print(key, body_sentiments[key])'''
    
    return avg_sentiment

def commentSentiment(urlT):
    #given post that mentions ticker, will calculate average sentiment of comments to that post and will return median comment date
    

    comments = [] 
    bodyComment = []
    comment_dates = []

    result = [0, -1]

    #get comments from sub
    try:
        post = reddit.submission(url=urlT)
        comments = post.comments            #returns iterable CommentForest object
    except:
        return result
    
    #save each comment to array
    for comment in comments:
        try: 
            bodyComment.append(comment.body)
            comment_dates.append(comment.created_utc)
        except:
            return result
    
    #median comments
    n = len(comment_dates)
    try:
        comment_dates.sort()
        mid = n // 2
        median = comment_dates[mid]
    except:
        return result
        
    sia = SIA()
    results = []
    for line in bodyComment:
        scores = sia.polarity_scores(line)
        scores['headline'] = line

        results.append(scores)
    
    df = pd.DataFrame.from_records(results)
    df.head()
    df['label'] = 0
    
    try:
        df.loc[df['compound'] > 0.1, 'label'] = 1
        df.loc[df['compound'] < -0.1, 'label'] = -1
    except:
        return result
    
    averageScore = 0
    position = 0
    while position < len(df.label)-1:
        averageScore = averageScore + df.label[position]
        position += 1

    averageScore = averageScore/len(df.label)

    
    result[0] = (averageScore)
    result[1] = median

    return result

## Date handling Functions:
def format_date(unix):
    #given date in epoch format, convert to YYYY-MM-DD format
    date = dt.datetime.fromtimestamp(unix)
    return date.strftime(date_format)


def add_days(date: str, t: int) -> str:
    date_obj = dt.datetime.strptime(date, date_format).date()

    new_date = date_obj + dt.timedelta(days=t) # Add t days

    return new_date.strftime(date_format)

def check_adjust_day(date):
    date_obj = dt.datetime.strptime(date, date_format).date()

    day = date_obj.weekday()

    if day == 5: #if the date is a saturday make it a friday
        date = add_days(date, -1)

    elif day == 6: #if date is a sunday make it monday
        date = add_days(date, 1)
    
    return date

def filter_date(range, date) -> bool:
    #returns true if given submission date is within the time range
    
    #Convert dates to dt objects
    start = dt.datetime.strptime(range[0], "%Y-%m-%d").date()
    end = dt.datetime.strptime(range[1], "%Y-%m-%d").date()
    date_obj = dt.datetime.strptime(date, "%Y-%m-%d").date()

    return start <= date_obj <= end

## Financial Functions:
def get_xday_ret(stock, date, x: int) -> float:
    date1 = add_days(date, 1)
    datex = check_adjust_day(add_days(date, x)) #x: 1,3,5,7,10
    

    counter = 0
    while True:
        stock_t0 = stock.history(period='1d', start=date, end=date1)

        if not stock_t0.empty or counter == 10:
            break

        date = date1
        date1 = add_days(date, 1)
        counter += 1
    
    counter = 0
    date1 = add_days(datex, 1)

    if (datex == date): ##if og date got incremented too much, then push date3 by one day
        datex = date1
        date1 = add_days(datex, 1)

    while True:
        stock_t1 = stock.history(period='1d', start=datex, end=date1)

        if not stock_t1.empty or counter == 10:
            break

        datex = date1
        date1 = add_days(datex, 1)
        counter += 1

    close0 = stock_t0["Close"].iloc[0]
    close1 = stock_t1["Close"].iloc[0]

    
    return round(close1/close0 -1, 4)


business_suffixes = ["Corp", "Corporation", "Inc", "LLC", "Limited", "Ltd", "Inc.", "Class A", "Class B", "Class C", ".", ","]
pattern = re.compile(rf'\s*(?:{"|".join(business_suffixes)})(?:[.,]?)\s*$', re.IGNORECASE)

def clean_company_name(name):
    #removes common business suffixes
    cleaned_name = pattern.sub('', name).strip()
    return cleaned_name