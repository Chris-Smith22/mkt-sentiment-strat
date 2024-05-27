# main.py - main executable

## Utility functions:
from utils import *

## Resources:
SUBREDDITS = ["wallstreetbets", "investing", "trading", "stocks", "stockmarket"]
sp_tickers = ['AMD', 'NVDA', 'AMC', 'SPY', 'TSLA', 'SMCI', 'AAPL',\
               'PYPL', 'DTE', 'JPM', 'SBUX', 'MSTR', 'GME', 'MSFT', \
                'LLY', 'QQQ', 'META', 'SNAP', 'INTC', 'MCD', 'GOOGL', \
                    'GOOG', 'TSM', 'VOO', 'NFLX', 'PLTR', 'KO', 'RTX', \
                        'LMT', 'IBM', 'BA']

## API Connection:
print("\n\n")
print(reddit.read_only)

stocks = {}
for ticker in sp_tickers:
    stocks[ticker] = []
    
    stock = yf.Ticker(ticker)
    stocks[ticker].append(stock) #0 is stock obj
    stocks[ticker].append(ticker) #search value1


### MAIN:
today = dt.date.today()
ytrd = today - dt.timedelta(days=1)
month = ytrd.strftime("%B")
yesterday = ytrd.strftime(date_format)

submission_statistics = []
search_range = [yesterday, yesterday] #1day range

counter = 1
try:
    for ticker in sp_tickers:
        n = len(sp_tickers)
        progress = round(counter/n, 4) * 100
        print(f"Progress: {progress}% - Ticker: {counter} out of {n} tickers.")
        
        d = {}
        query = f"(title:{stocks[ticker][1]} OR selftext:{stocks[ticker][1]})"  # OR selftext:{stocks[ticker][2]} OR title:{stocks[ticker][2]})"

        for subname in SUBREDDITS:
            for submission in reddit.subreddit(subname).search(query, syntax='lucene', limit=200, time_filter="year"):
                #Date of submission  
                sub_date = format_date(submission.created_utc)  
            
                if not filter_date(search_range, sub_date):     #skip post if not in date range
                    continue
                
                d = {}
                d['ticker'] = ticker
                d['date'] = sub_date
                                
                #Sentiment analysis:    
                d['post_sentiment'] = postSentiment(submission.url)
                commentinfo = commentSentiment(submission.url)
                d['comment_sentiment_average'] = commentinfo[0]
                if d['comment_sentiment_average'] == 0:
                    continue
                
                #Popularity factors:
                d['num_comments'] = submission.num_comments
                d['score'] = submission.score
                d['upvote_ratio'] = submission.upvote_ratio
                d['num_crossposts'] = submission.num_crossposts
                if commentinfo[1] != -1:
                    d['delta'] = (commentinfo[1] - submission.created_utc)/86400         #difference in submission post date and median comment in days
                else:
                    continue

                #extra info
                d['domain'] = submission.domain
                d['url'] = submission.url
                submission_statistics.append(d)
        
        counter += 1
except prawcore.exceptions.TooManyRequests as e:
        print("too many requests broski.....\n\n\n\n")    

finally:
    dfSentimentStocks = pd.DataFrame(submission_statistics)
    

    if not os.path.exists(f"./results/{month}"):
        os.mkdir(f"./results/{month}")

    dfSentimentStocks.to_csv(f"./results/{month}/{yesterday}_SA.csv", index=False)
    print("\n\n\nDONE.")

