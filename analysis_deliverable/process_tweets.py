import sqlite3
import scipy.stats as stats

conn = sqlite3.connect('../data_deliverable/data/tesla_tweets.db')
c = conn.cursor()
tweets_text = c.execute('SELECT text FROM tesla_tweets')

#this file will hold the text column of the same rows as the tesla_tweets.db file.
#converted to .txt format for compatibility with NLP API
file_pointer = open("tweets_processing_files/tweets.txt", "w")
row_counter = -1
for tweet in tweets_text:
    #parse out 2019 data to get range of dates we are interested in
    row_counter +=1
    if row_counter == 17 or row_counter == 20:
        continue
    char_row = ''
    for letter in str(tweet):
        char_row += letter
    #write one tweet per row
    file_pointer.write(char_row)
    file_pointer.write('\n')

#for each day of tweets, get the number of tweets per day and store in array
tweets_date = c.execute('SELECT date FROM tesla_tweets')
row_counter = -1
date_list = []
for date in tweets_date:
    row_counter +=1
    #as above, parse out 2019 data
    if row_counter == 17 or row_counter == 20:
        continue
    date_list.append(date)

#read in the output from the NLP API. The below file will have each tweet and its sentiment score
file_pointer = open("tweets_processing_files/api_output.txt", "r")
score_list = []
for row in file_pointer:
    #parse out the score for each tweet
    score = str(row)[1:2]
    score_list.append(score)

#create a file that stores each tweets score, and its corresponding date. 
file_pointer = open("tweets_processing_files/scores_and_dates.txt", "w")
for i in range(len(score_list)):
    file_pointer.write(str(score_list[i]))
    file_pointer.write(", ")
    file_pointer.write(str(date_list[i]))
    file_pointer.write('\n')


file_pointer = open("tweets_processing_files/scores_and_dates.txt", "r")
date_dictionary = {}
#dictionary structure is (key: date, value: (count, score_sum)) where count is the number
#of tweets for the given date and score sum is the cumulative NLP score for all the tweets 
#created on that date
for row in file_pointer:
    str_row = str(row)
    score = int(str_row[0:1])
    date = str_row[5:15]
    if date in date_dictionary:
        value = date_dictionary[date]
        count = value[0]
        sentiment_sum = value[1]
        count +=1
        sentiment_sum += score
        date_dictionary[date] = (count, sentiment_sum)
    else:
        date_dictionary[date] = (1, score)

#compute the average sentiment score for each date and write to the file
sentiment_list = []
file_pointer = open("tweets_processing_files/date_sentiment.txt", "w")
for key in date_dictionary:
    file_pointer.write(key)
    file_pointer.write(", ")
    count = date_dictionary[key][0]
    sentiment_sum = date_dictionary[key][1]
    average_sentiment_sum = sentiment_sum/count
    file_pointer.write(str(average_sentiment_sum))
    file_pointer.write('\n')
    sentiment_list.append((key, average_sentiment_sum))

#need to get stock price relative to index a certain number of days after these days
#since tweet data is from Jan 1 2020 to Feb 3 2020, get stock data exactly 30 days after ie 
    #Jan 31 2020 to March 5 2020

#get low, high russell close stock price in the database
russell_close_list = []
conn = sqlite3.connect('../data_deliverable/data/data.db')
c = conn.cursor()
russell_close = c.execute('SELECT close FROM russell_stock_data')
lo = float("inf")
hi = -1
for price in russell_close:
    price = price[0] #parse from tuple format
    russell_close_list.append(price)
    if price < lo:
        lo = price
    if price > hi:
        hi = price

russell = c.execute('SELECT date FROM russell_stock_data')
russell_date = []
for date in russell:
    russell_date.append(date)

russell_score = []
for i in range(len(russell_date)):
    date = str(russell_date[i][0])
    year = date[6:10]
    month = date[0:2]
    day = date[3:5]
    if date == '01/31/2020' or month == '02' and year == '2020' or date == '03/01/2020' or date == '03/02/2020' or date == '03/03/2020' or date == '03/04/2020' or date == '03/05/2020':
        #normalize russell close price relative to min and max russell close for days in question
        russell_score.append((date, (russell_close_list[i] - lo)/(hi - lo)))

#get lo, hi tesla close stock price in the database
tesla_close_list = []
conn = sqlite3.connect('../data_deliverable/data/data.db')
c = conn.cursor()
tesla_close = c.execute('SELECT close FROM tesla_stock_data')
lo = float("inf")
hi = -1
for price in tesla_close:
    price = price[0] #parse from tuple format
    tesla_close_list.append(price)
    if price < lo:
        lo = price
    if price > hi:
        hi = price

tesla = c.execute('SELECT date FROM tesla_stock_data')
tesla_date = []
for date in tesla:
    tesla_date.append(date)

#compute % of where tesla is on scale of lo -> hi for days in question
tesla_score = []
for i in range(len(tesla_date)):
    date = str(tesla_date[i][0])
    year = date[6:10]
    month = date[0:2]
    day = date[3:5]
    if date == '01/31/2020' or month == '02' and year == '2020' or date == '03/01/2020' or date == '03/02/2020' or date == '03/03/2020' or date == '03/04/2020' or date == '03/05/2020':
        #normalize tesla close price on scale of lo -> hi for days in question
        tesla_score.append((date, (tesla_close_list[i] - lo)/(hi - lo)))

#store a number for each day of normalized_tesla_close - normalized_russell_close  
#this will be tesla stock price relative to russell index
relative_scores = []
for i in range(len(tesla_score)):
    if tesla_score[i][0] != russell_score[i][0]:
        print("dates do not match up")
    else:
        #tuple of date, (russell_normalized - tesla_normalized) ie relative stock price
        relative_scores.append((tesla_score[i][0], russell_score[i][1] - tesla_score[i][1]))

file_pointer = open("tweets_processing_files/relative_scores.txt", "w")
for i in range(len(relative_scores)):
    file_pointer.write(str(tesla_score[i][0]))
    file_pointer.write(", ")
    file_pointer.write("tesla score is ")
    file_pointer.write(str(tesla_score[i][1]))
    file_pointer.write(", ")
    file_pointer.write("russell score is ")
    file_pointer.write(str(russell_score[i][1]))
    file_pointer.write(", ")
    file_pointer.write("relative score is ")
    file_pointer.write(str(relative_scores[i][1]))
    file_pointer.write('\n')

#create cross table of the average sentiment, relative stock price

#create table of 
    # relative score, relative score, ....
    # avg sentiment, avg sentiment, ....
#lined up where the relative scores are 30 days after the sentiment scores

#remove rows from date sentiment that are not 30 days after a relative score
relative_scores #format (date, score) where date = MM/DD/YYYY
sentiment_list #format (date, avg sentiment score) where date = YYYY-MM-DD
relative_scores_dictionary = {} #format: key = MM/DD/YYYY as str, value = avg sentiment score
for i in range(len(relative_scores)):
    relative_scores_dictionary[str(relative_scores[i][0])] = relative_scores[i][1]
cross_table_scores = []
cross_table_sentiment = []
cross_table_date_scores = []
cross_table_date_sentiment = []
for i in range(len(sentiment_list)):
    month = sentiment_list[i][0][5:7]
    day = int(sentiment_list[i][0][8:10])
    if day + 30 > 31 and month == "01":
        find_scores_month = "02"
        find_scores_day = str((day + 30) - 31)
        
    elif month == "02":
        find_scores_month = "03"
        find_scores_day = str((day + 30) - 28)
    else:
        find_scores_month = month
        find_scores_day = str(day + 30)
    find_date = find_scores_month + '/' + find_scores_day + "/2020"
    if find_date in relative_scores_dictionary:
        cross_table_scores.append(relative_scores_dictionary[find_date])
        cross_table_sentiment.append(sentiment_list[i][1])
        cross_table_date_scores.append(find_date)
        cross_table_date_sentiment.append(month + '/' + str(day) + "/2020")
        
file_pointer = open("tweets_processing_files/cross_table_info.txt", "w")
file_pointer.write("relative score date should be exactly 30 days after sentiment date \n")
for i in range(len(cross_table_scores)):
    file_pointer.write("relative score is ")
    file_pointer.write(str(cross_table_scores[i]))
    file_pointer.write(", avg sentiment is ")
    file_pointer.write(str(cross_table_sentiment[i]))
    file_pointer.write(", date for relative score is ")
    file_pointer.write(cross_table_date_scores[i])
    file_pointer.write(", date for sentiment is ")
    file_pointer.write(cross_table_date_sentiment[i])
    file_pointer.write('\n')

cross_table = [cross_table_scores] + [cross_table_sentiment]

#perform stats analysis on the cross table and print results
chi_squared, p_value, degrees_of_freedom, expected = stats.chi2_contingency(cross_table)
print("chi_squared is ", chi_squared, ", p value is ", p_value, ", degrees of freedom is ", degrees_of_freedom)