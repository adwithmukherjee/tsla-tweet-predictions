import pandas as pd
import sqlite3
import math

# Create connection to database
conn = sqlite3.connect('data.db')
c = conn.cursor()

#helper method to remove $ symbol from numerical data
def remove_dollar_symbol(column):
    for i in range(len(column)):
        column[i] = column[i][1:]
    return column

#helper method to reformat russell date so that it matches tesla date format
def reformat_date(column):
    for i in range(len(column)):
        date = column.loc[i]
        year = date[0:4]
        month = date[5:7]
        day = date[-2:]
        column[i] = month + "/" + day + "/" + year
    return column

#read Tesla data
data = pd.read_csv("Tesla.csv")

#clean data
data['Close/Last'] = remove_dollar_symbol(data['Close/Last'].copy())
data['Open'] = remove_dollar_symbol(data['Open'].copy())
data['High'] = remove_dollar_symbol(data['High'].copy())
data['Low'] = remove_dollar_symbol(data['Low'].copy())

#read Russell data
data2 = pd.read_csv("Russell3000.csv")

#clean data
data2['Date'] = reformat_date(data2['Date'].copy())

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "tesla_stock_data";')
c.execute('DROP TABLE IF EXISTS "russell_stock_data";')

#Create tables in the database and commit
c.execute('CREATE TABLE tesla_stock_data(date primary key not null, close float not null, \
        volume int not null, open float not null, high float not null, low float not null)')
c.execute('CREATE TABLE russell_stock_data(date primary key not null, close float not null, \
        volume int not null, open float not null, high float not null, low float not null)')
conn.commit()

#populate database tables with data and commit
for i in range(len(data)):
    date = data.loc[i, 'Date']
    year = date[-4:]
    #only add data within time range of interest to database
    if (year == '2019' or year == '2020'):
        c.execute('INSERT INTO tesla_stock_data VALUES (?, ?, ?, ?, ?, ?)', \
        (data.loc[i, 'Date'], data.loc[i, 'Close/Last'], data.loc[i, 'Volume'].astype(float), \
        data.loc[i, 'Open'], data.loc[i, 'High'], data.loc[i, 'Low']))

for i in range(len(data2)-1, -1, -1):
    #remove days where russell data is not available (25 instances over 2 years)
    if (not math.isnan(data2.loc[i, 'Close'])):
        c.execute('INSERT INTO russell_stock_data VALUES (?, ?, ?, ?, ?, ?)', \
        (data2.loc[i, 'Date'], data2.loc[i, 'Close'], data2.loc[i, 'Volume'], \
        data2.loc[i, 'Open'], data2.loc[i, 'High'], data2.loc[i, 'Low']))
conn.commit()

#create table to store joined results so that russell and tesla data are in same place
c.execute('DROP TABLE IF EXISTS "combined_stock_data";')
c.execute('CREATE TABLE combined_stock_data(Date primary key not null, TeslaClose float not null, \
            TeslaVolume int not null, TeslaOpen float not null, TeslaHigh float not null, TeslaLow float not null, \
            RussellClose float not null, RussellVolume int not null, RussellOpen float not null, \
            RussellHigh float not null, RussellLow float not null)')
conn.commit()

#execute sql join query and store in table
c.execute('''SELECT t.date, t.close, t.volume, t.open, t.high, t.low, r.close, r.volume, r.open, \
        r.high, r.low FROM tesla_stock_data t JOIN russell_stock_data r WHERE t.date = r.date''')
combined_data = c.fetchall()
for i in range(len(combined_data)):
    c.execute('INSERT INTO combined_stock_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', \
        (combined_data[i][0], combined_data[i][1], combined_data[i][2], combined_data[i][3], \
        combined_data[i][4], combined_data[i][5], combined_data[i][6], combined_data[i][7], \
        combined_data[i][8], combined_data[i][9], combined_data[i][10]))
conn.commit()