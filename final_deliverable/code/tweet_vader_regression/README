This folder includes: 
  
  scrape_tweets.py: A script for scraping Tweets directly from Twitter using Selenium. Creates a database of Tweets called tesla_tweets.db
  
  analyze_sentiment.py: A script that assigns positive, negative, neutral sentiment scores to each row of the "tweets" table in tesla_tweets.db. It then reduces 
    this table by date to get the average values for pos, neg, neu sentiment, as well as likes and comments, for Tweets on each available date. It then uses scraped 
    TSLA stock data to add the percent change in share price for each date to the table. Saves the resultant table of sentiment values and stock data for each date in 
    a file called sentiments.csv
    
  multiple.py:  Runs ordinary least squares regression on the sentiments.csv dataset. It uses the most significant independent variables ["pos","neg"] (average positive 
  and negative sentiment scores) and a dependent variable of ["pc"], or percent change in TSLA share price. 
