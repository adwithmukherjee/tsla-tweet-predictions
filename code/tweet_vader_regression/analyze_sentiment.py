import sqlite3
from numpy.core.numeric import NaN
import pandas as pd
from pandas.core.frame import DataFrame
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import io
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np


url="https://raw.githubusercontent.com/CS1951A-S21-Brown/MADS_final_project/main/data_deliverable/data/Tesla.csv?token=AN4INNLKZCX2YK2AIZES55LAOJIEY"
s=requests.get(url).content
tesla_df=pd.read_csv(io.StringIO(s.decode('utf-8')))


def pc(x):
    open = float(x['Open'].replace("$",""))
    close = float(x['Close/Last'].replace("$",""))
    return (close-open)/open

def date(x):
   date_value = datetime.strptime(x, "%m/%d/%Y")
   return date_value.strftime("%Y-%m-%d %H:%M:%S")

tesla_df["percent_change"] = tesla_df.apply(pc, axis=1)
tesla_df["Date"] = tesla_df["Date"].apply(date)

##########################
conn = sqlite3.connect('tesla_tweets.db')
c = conn.cursor()


df = pd.read_sql_query("SELECT * from tesla_tweets ORDER BY date ASC", conn)


analyzer = SentimentIntensityAnalyzer()


df['text'] = df['text'].str.replace('\n', ' ').replace("'","")

 
def analyze_pos(s1):
    return analyzer.polarity_scores(s1)["pos"]
def analyze_neg(s1):
    return analyzer.polarity_scores(s1)["neg"]
def analyze_neutral(s1):
    return analyzer.polarity_scores(s1)["neu"]

df['pos'] = df['text'].apply(analyze_pos)
df['neg'] = df['text'].apply(analyze_neg)
df['neu'] = df['text'].apply(analyze_neutral)

print(df.head())

dates = {}

current_date = None

for index,row in df.iterrows():
    current_date = row['date']
    if(current_date not in dates):
        dates[current_date] = [row['comments'], row['likes'], row['pos'], row['neg'], row['neu'],1]
    else: 
        new_data = [row['comments'], row['likes'], row['pos'], row['neg'], row['neu'],1]
        
        dates[current_date] = [a + b for a,b in zip(dates[current_date], new_data)]


dates_df = DataFrame.from_dict(dates, orient='index', columns=['comments', 'likes', 'pos', 'neg', 'neu', 'num_tweets'])

dates_df['pos'] = dates_df['pos']/dates_df['num_tweets']
dates_df['neg'] = dates_df['neg']/dates_df['num_tweets']
dates_df['neu'] = dates_df['neu']/dates_df['num_tweets']
dates_df['com'] = dates_df['pos'] + dates_df['neg']
# dates_df['neg'] = dates_df.apply(lambda x: float(float(x['neg']) / float(x['num_tweets'])))
# dates_df['neu'] = dates_df.apply(lambda x: float(float(x['neu']) / float(x['num_tweets'])))

stock_data = []

for index,row in dates_df.iterrows():
    row = tesla_df[tesla_df["Date"] == index]
    if(row.empty):
        stock_data.append(None)
    else:
        # if float(row["percent_change"]) >= 0:
        #     stock_data.append(1)
        # else:
        #     stock_data.append(-1)
        stock_data.append(float(row["percent_change"]))

dates_df["pc"] = stock_data




result = dates_df[dates_df["pc"].notnull()]

#result.to_sql('sentiments', con=conn, if_exists='replace')



conn.commit()
conn.close()

#####



# ax = dates_df.plot.scatter(x="neg", y="pc")

# ax.set_xlabel("Average Negative Sentiment Score on TSLA Tweets")
# ax.set_ylabel("Percent Change in TSLA Stock Price")
# plt.title("Average TSLA Tweet sentiment as an indicator of TSLA stock price ")
# plt.show()

result.to_csv('./sentiments.csv',index=False)