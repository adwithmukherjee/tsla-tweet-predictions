import time 
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import sqlite3

browser = webdriver.Chrome()

base_url = u'https://twitter.com/search?q='
query = u'TSLA%20until%3A2021-01-01%20since%3A2020-01-01%20-filter%3Areplies'
url = base_url + query

browser.get(url)
time.sleep(2)
body = browser.find_element_by_tag_name('body')

conn = sqlite3.connect('tesla_tweets.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "tweets";')

c.execute('CREATE TABLE tweets (date DATE, author VARCHAR(100), text VARCHAR(1000), comments INTEGER, likes INTEGER);')
conn.commit()


tweets = []
#print(tweet_author.text)

def step():
    tweet_divs = browser.find_elements_by_xpath("//div[@data-testid='tweet']") 
    for div in tweet_divs:
        date = div.find_element_by_xpath(".//div[2]/div/div/div/div/a/*")
        date = datetime.strptime(date.text, "%b %d, %Y")
        tweet_author = div.find_element_by_xpath(".//div[2]/div/div/div/div/div/a/div/div[2]/*").text.replace("(","").replace(")","").replace('"','')
        tweet_text = div.find_element_by_xpath(".//div[2]/div[2]/div[1]").text.replace("(","").replace(")","").replace('"','')
        comments = div.find_element_by_xpath(".//div[2]/div[2]/div[3]/div[1]/*")
        likes = div.find_element_by_xpath(".//div[2]/div[2]/div[3]/div[3]/*")
        clean_likes = likes.text
        if(likes.text==""):
            clean_likes = "0"
        clean_likes = int(clean_likes.replace(".", "").replace("M", "00000").replace("K", "00"))
        clean_comments = comments.text
        if(comments.text==""):
            clean_comments = "0"
        clean_comments = int((clean_comments).replace(".", "").replace("M", "00000").replace("K", "00"))
        tweet = [date, tweet_author, tweet_text, clean_comments, clean_likes]
        tweets.append(tweet)
  
start = datetime.strptime("1 January, 2020", "%d %B, %Y")

for i in range(365):

    end = start + timedelta(days=1)
    start_string = start.strftime("%Y-%m-%d")
    end_string = end.strftime("%Y-%m-%d")

    query = u'TSLA%20until%3A{}%20since%3A{}%20-filter%3Areplies'.format(end_string, start_string)
    url = base_url + query

    if i%30 == 0:
        browser.quit()
        browser = webdriver.Chrome()
     
    browser.get(url)
    time.sleep(2)
    body = browser.find_element_by_tag_name('body')

    start = end

    for j in range(40):
        if (j%12 == 0):
            time.sleep(0.8)
            step()
            body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)

    print(len(tweets))
    df = pd.DataFrame(tweets, columns=["date", "author", "text", "num_comments", "num_likes"])
    print(df)

    for index, row in df.iterrows():
        #c.execute('INSERT INTO companies VALUES("{}", "{}", "{}");'.format(row["Symbol"], row["Name"], row["HQ"]))
        c.execute('INSERT INTO tweets VALUES("{}", "{}", "{}", {}, {});'.format(row["date"], row["author"], row["text"], row["num_comments"], row["num_likes"]))

    conn.commit()