# Data Spec
### data.db (stock data)
The data.db file is composed of 3 tables. The first is tesla_stock_data, which has the following schema:  

date primary key not null, close float not null, volume int not null, open float not null, high float not null, low float not null  

The second table is russell_stock_data, which has the same schema as the tesla_stock_data table. The third table is combined_stock_data, which joins the tesla_stock_data and russell_stock_data tables on the primary key day. It has the following schema:  

Date primary key not null, TeslaClose float not null, TeslaVolume int not null, TeslaOpen float not null, TeslaHigh float not null, TeslaLow float not null, RussellClose float not null, RussellVolume int not null, RussellOpen float not null, RussellHigh float not null, RussellLow float not null  

It contains all of the same columns as tesla_stock_data and russell_stock_data except with only one copy of the date. 
Several assumptions about data types were made when constructing the database. Volume is assumed to be an int, and other numeric values are assumed to be represented by floats. All values are required to be not null. 
The join query is based on the assumption that the tesla_stock_data and russell_stock_data will have most days of data available. The russell_stock_data table was slightly less complete, having data for 25 less days than the tesla_stock_data table over the two year time period studied. For now, the days where only tesla data is available are omitted from the combined_stock_data table as comparisons between the two stocks cannot be made and therefore the data will not be helpful for our use case. 
Note that the Russell3000.csv and Tesla.csv files are input data collected online from outside sources. These are included for reference, and are used to create the data.db file. More information about this process can be found in the tech report. 

### result.csv (Stocktwits data)
Stocktwits data only has one table which looks like this:   
   messages_id                       INTEGER  NOT NULL PRIMARY KEY   
   messages_body                     VARCHAR(431) NOT NULL  
   messages_created_at               VARCHAR(20) NOT NULL  
   messages_user_id                  INTEGER  NOT NULL  
   messages_user_username            VARCHAR(19) NOT NULL  
   messages_entities_sentiment_basic VARCHAR(7)  

We use the message_id as key, and since the Stocktwits API will only give 30 stocks in one call we don’t want duplicate messages. We are making the assumption that every commenter will have a sentiment such as “Bullish” or “Bearish.” However, there are tweets that don’t explicitly mention sentiment which creates some gaps. Also, we’re noticing on the website that a lot of bots are centered around creating an illusion of sentiment, hence we also store user_id of a post so we can later on see how to add bias depending on how many unique messages we accumulate. 

### tesla_tweets.db (Twitter data)
tesla_tweets.db has one table called “tweets”:   
	date:  		DATE  
	author: 	VARCHAR(100)  
	text: 		VARCHAR(500)  
	comments:	INTEGER  
	likes:	 	INTEGER  

Where a combination of author and text serve as the primary key. This data is scraped from Twitter using Selenium and is equivalent to retrieving tweets by searching “$TSLA” on twitter for certain dates. We will use this tweet data to evaluate sentiment in the analysis part of the project. Comments and likes are recorded to measure the visibility of the post, and the author is recorded so that an author and their tweets can easily be removed from the database for further cleaning. 

