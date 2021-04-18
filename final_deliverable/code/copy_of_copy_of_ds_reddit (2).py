# -*- coding: utf-8 -*-
"""Copy of Copy of DS Reddit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ipcpaSXDmaEQKEjAvcSoJjwO-vdVPyKv
"""

import requests
import pandas as pd
query="TSLA" #Define Your Query
url = f"https://api.pushshift.io/reddit/search/comment/?q={query}"
request = requests.get(url)
json_response = request.json()
#json_response
#df = pd.read_json('/tsla.json')

from json.decoder import JSONDecodeError
def get_pushshift_data(data_type, **kwargs):
    try:
      base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
      payload = kwargs
      request = requests.get(base_url, params=payload)
      return request.json()
    except JSONDecodeError:
      return None

data_type="comment"     # give me comments, use "submission" to publish something
query="TSLA"          # Add your query
duration="720d"        # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
size=500             # maximum 1000 comments
sort_type="created_utc"       # Sort by score (Accepted: "score", "num_comments", "created_utc")
sort="desc"             # sort descending
aggs="subreddit"
get_pushshift_data(data_type=data_type,     
                   q=query,   
                   before="1609379830",              
                   after="1546307830",          
                   size=size,               
                   sort_type=sort_type,
                   sort=sort)

!pip install nltk
import pandas as pd
import nltk
import statistics
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
day = 6
new_words = {
    'yolo': 3.0,
    'bullish': 10.0,
    'moon':10.0,
    'gains':3.0,
    'hold':10.0,
    'ape':10.0,
    'tendies':10.0,
    'drop':-10.0,
    'bear':-10.0,
    'bag hold':-10.0,
    'calls':10.0,
    'puts': -10.0,
    'jpow': 10.0,
    'stimulus': 10.0,
    'stimmy': 10.0,
    'theta': -5.0,
    'short squeeze': 5.0,
    'squeeze': 5.0,
    'parabolic' : 5.0,
    'lambo': 5.0,
    'faang': 10.0,
    'crush':5.0,
    'earnings crush':5.0,
    'tweet':10.0,
    'elon':5.0,
    'papa': 5.0,
    'china':5.0,
    'expand':5.0,
    'credits':5.0,
    'bonus':5.0,
    'discount':10.0,
    'sale':10.0,
    'cheap':10.0,
    'too' : -5.0,
    'too expensive':-10.0,
    'insane': 10.0,
    'strong': 10.0,
    'bounce':10.0,
    'deadcat': -5.0,
    'dead cat': -5.0,
    'rsi down': 10.0,
    'bounce back':10.0,
    'news':5.0,
    'rip':-5.0,
    'high':10.0,
    'new high':10.0,
    'ath':10.0,
    'upgrade':10.0,
    'cathie wood':10.0,
    'ark':10.0,
    'goldman':10.0,
    'morgan': 10.0
  }
SIA = SentimentIntensityAnalyzer()
SIA.lexicon.update(new_words)
results_daily = []
for i in range (0,720):
  #get current day here
  check = False
  end_time = str(836-i)+"d"
  data_type="comment"     # give me comments, use "submission" to publish something
  query="TSLA"          # Add your query
  duration= str(837 - i)+"d"    # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
  size=1000             
  sort_type="created_utc"       # Sort by score (Accepted: "score", "num_comments", "created_utc")
  sort="desc"             # sort descending
  aggs="subreddit"
  if day +1 == i +2:
    #print("skip2")
    
    day = day + 7
    
    continue
  if day == i +2:
    #print("skip")
    
    #day = day + 7
    #print(i)
    continue
  
  data = get_pushshift_data(data_type=data_type,
                          q=query,
                          before=end_time,
                          after=duration,
                          size=size,
                          aggs=aggs)
  
  if data == None:
    results_daily.append(0)
    continue
  if(len(data.values())==0):
    results_daily.append(0)
    continue
  data = list(data.values())[0]
  
    
  #print(data)
  df = pd.DataFrame.from_records(data)
  #print(df["created_utc"][0])
  #print(i+2)
  #print(df)
  if df.empty:
    results_daily.append(0)
    continue
  
  df = pd.DataFrame.from_records(data)[["author", "subreddit", "score", "body", "permalink"]]
#df
  

  
  titles = df['body']

  results = []
  sum = 0.0
  for title in titles:
      pol_score = SIA.polarity_scores(title.lower())
      pol_score['title'] = title
      sum += pol_score['compound']
      results.append(pol_score['compound'])
      #print(pol_score)
    #print(title)
  
  avg_day = sum / len(titles)

  #print(avg_day)
  rsize = len(results)
  
  #print(statistics.median(results))
  toAdd = statistics.median(results)
  if avg_day > toAdd:
    toAdd = avg_day
  print(toAdd)
  results_daily.append(toAdd)
  

print(results_daily)

!pip install scipy
from scipy import stats as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform

results_daily = [0.104341, 0.296, 0.33685, 0.4329, 0.22811379310344818, 0.18499999999999994, 0.20475789473684217, 0.20614, 0.8695999999999999, 0.2855382352941177, 0.4696, 0.7628, 0.30225, 0.5370999999999999, 0.3071, 0.23998799999999995, 0.2263, 0.4019, 0.5623, 0.5402, 0.2985663043478261, 0.13609100000000005, 0.4404, 0.21418275862068964, 0.3612, 0.11928235294117649, 0.40959999999999996, 0.377, 0.68, 0.17930270270270265, 0.12118837209302326, 0.7216, 0.2263, 0.3597, 0.18422903225806447, 0.4767, 0.13986142857142853, 0.20175277777777784, 0.32332758620689656, 0.28459999999999996, 0.19373799999999997, 0.5106, 0.26093999999999995, 0.38754999999999995, 0.130464, 0.31294999999999995, 0.2275530000000002, 0.27169600000000005, 0.7466, 0.2974488095238095, 0.3612, 0.20555599999999988, 0.37070000000000003, 0.3612, 0.28005, 0.4107, 0.46655, 0.35865, 0.4201, 0.17011728395061732, 0.05535479452054793, 0.2686, 0.257369512195122, 0.44325000000000003, 0.12076999999999995, 0.2917390000000002, 0.13701600000000003, 0.3182, 0.08367636363636362, 0.16412463768115942, 0.10936477272727273, 0.22035, 0.1552908163265306, 0.23565, 0.17555800000000002, 0.3349, 0.2354, 0.16748076923076924, 0.39990000000000003, 0.2082, 0.3071, 0.09356300000000001, 0.25335, 0.4404, 0.27544300000000005, 0.29510000000000003, 0.27647799999999995, 0.43095, 0.3182, 0.17105399999999998, 0.2828, 0.24336582278481006, 0.3182, 0.4215, 0.24564999999999998, 0.2021, 0.296, 0.064671, 0.34535, 0.33765, 0.3674, 0.15589, 0.14101699999999995, 0.13271700000000006, 0.17770000000000002, 0.19681700000000013, 0.4019, 0.164351, 0.39690000000000003, 0.06769799999999997, 0.138168, 0.23600099999999993, 0.31255, 0.3224558823529411, 0.3189, 0.55105, 0.2687232323232326, 0.34, 0.5994, 0.3286, 0.1949608108108108, 0.158547, 0.4496, 0.1997, 0.5963, 0.4404, 0.24975, 0.3612, 0.17876562500000004, 0.22560799999999998, 0.59605, 0.3989, 0.4003, 0.296, 0.2785297297297298, 0.38155, 0.19425699999999999, 0.3612, 0.33259400000000006, 0.35065, 0.270187, 0.4019, 0.2575310000000002, 0.2096666666666666, 0.24319600000000002, 0.4404, 0.137148, 0.22849999999999998, 0.5423, 0.20098400000000005, 0.2436633333333333, 0.37929999999999997, 0.43095, 0.65785, 0.28086551724137937, 0.3818, 0.3976, 0.431, 0.07749999999999999, 0.11004927536231887, 0.08884647887323943, 0.3818, 0.3182, 0.20355675675675675, 0.3223282051282052, 0.16909879518072288, 0.2023, 0.56565, 0.12056458333333331, 0.09278055555555556, 0.19575, 0.20933548387096773, 0.4404, 0.5423, 0.008172727272727278, 0.00909791666666667, 0.4215, 0.23361666666666667, 0.0, 0.2353259259259259, 0.34975, 0.4588, 0.38075000000000003, 0.41169999999999995, 0.2128139534883721, 0.06626666666666671, 0.0, 0.13399298245614033, 0.20163333333333333, 0.09125900000000005, 0.34748831168831157, 0.16471400000000005, 0.2161144578313253, 0.34, 0.2835711111111111, 0.1174783505154639, 0.19002100000000005, 0.6523, 0.7172, 0.5378000000000001, 0.4939, 0.23481830985915494, 0.1771, 0.3970782608695652, 0.6638, 0.3933, 0.56775, 0.06585333333333332, 0.5112, 0.10226027397260273, 0.3071, 0.17397599999999996, 0.17357000000000003, 0.18835100000000005, 0.07829799999999999, 0.21820100000000012, 0.49295, 0.25609565217391295, 0.05068837209302324, 0.2122671052631579, 0.3612, 0.2732, 0.2646, 0.39395, 0.31135, 0.25745799999999996, 0.4945, 0.3506, 0.4404, 0.3818, 0.22034000000000004, 0.55635, 0.13636900000000005, 0.41655, 0.4404, 0.4404, 0.7130000000000001, 0.4246, 0.31720000000000004, 0.296, 0.3002924050632912, 0.50965, 0.4404, 0.0812375, 0.5678000000000001, 0.1415209876543211, 0.15808900000000004, 0.2101342857142857, 0.4849, 0.41664999999999996, 0.20853099999999997, 0.3902, 0.5068999999999999, 0.4496, 0.19155, 0.3506, 0.13356799999999996, 0.39135, 0.5719, 0.18683599999999995, 0.3612, 0.2746159999999999, 0.2372, 0.39135, 0.3612, 0.14227299999999998, 0.4215, 0.40645, 0.17382099999999998, 0.4215, 0.26025, 0.3071, 0.43095, 0.156241, 0.19556100000000007, 0.5480499999999999, 0.16819699999999999, 0.15047599999999994, 0.19741400000000012, 0.4302, 0.315483, 0.10692899999999998, 0.43095, 0.19619999999999999, 0.17951500000000004, 0.052835, 0.09819400000000002, 0.0, 0.07584500000000002, 0.17057200000000003, 0.47485, 0.16149800000000006, 0.35115, 0.12063599999999995, 0.29569999999999996, 0.1663929999999999, 0.4588, 0.40705, 0.39055, 0.28092200000000017, 0.2593, 0.296, 0.039927, 0.049796999999999994, 0.19504700000000003, 0.10036499999999998, 0.18399, 0.206498, 0.19449499999999995, 0.13833599999999993, 0.15211700000000003, 0.10021799999999999, 0.0, 0.16212999999999994, 0.0, 0.0, 0.0, 0.0, 0.017593, 0.044818999999999984, 0.063696, 0.016646, 0.0, 0.10171000000000005, 0.068419, 0.06590200000000004, 0.18374600000000002, 0.0, 0.10236500000000001, 0.170062, 0.19911699999999996, 0.12914899999999999, 0.06029700000000001, 0.1770163043478261, 0.08970399999999999, 0.18747699999999998, 0.296, 0.042332999999999954, 0.12501200000000004, 0.0, 0.0, 0.06123400000000001, 0.2732, 0.381, 0.2109, 0.11814299999999997, 0.20965, 0.06500500000000002, 0.233215, 0.14055, 0.16731499999999996, 0.16630200000000006, 0.102417, 0.20328800000000002, 0.23815, 0.42545, 0.10157299999999997, 0.28623400000000015, 0.139987, 0.3071, 0.11062900000000003, 0.25119400000000003, 0.3071, 0.5037, 0.31076600000000004, 0.3559, 0.44994999999999996, 0.25, 0.21415, 0.145604, 0.17960199999999993, 0.21337699999999998, 0.14563800000000002, 0.3069, 0.2168910000000001, 0.17934599999999995, 0.28459999999999996, 0.10776300000000003, 0.0, 0.16974999999999998, 0.42115, 0.39254999999999995, 0.3221, 0.31855, 0.25975, 0.2616, 0.102179, 0.4496, 0.41585, 0.131192, 0.12314600000000006, 0.4019, 0.318, 0.5921000000000001, 0.264158, 0.18705, 0.143339, 0.11315799999999995, 0.27925, 0.17364500000000002, 0.3255, 0.42625, 0.14213700000000004, 0.06969199999999998, 0.296, 0.10401900000000001, 0.4067, 0.25018000000000007, 0.296, 0.245632, 0.24737299999999995, 0.2572950000000001, 0.23261499999999993, 0.17017600000000005, 0.22564299999999998, 0.296, 0.19123299999999993, 0.17018700000000006, 0.07973599999999999, 0.3612, 0.12986699999999998, 0.2376130000000001, 0.23547900000000002, 0.19345400000000001, 0.21056699999999992, 0.22051099999999985, 0.26115, 0.288274, 0.20558999999999997, 0.15589299999999992, 0.18286299999999994, 0.26973400000000003, 0.19602, 0.273, 0.16131799999999996, 0.18622899999999995, 0.19743, 0.212591, 0.09394200000000005, 0.17954300000000006, 0.14997099999999994, 0.3612, 0.14618800000000007, 0.37095, 0.13930700000000001, 0.12480199999999998, 0.0, 0.20203800000000005, 0.296, 0.21290599999999998, 0.050797999999999996, 0.3071, 0.150244, 0.18995399999999996, 0.20223500000000005, 0.205269, 0.15536499999999998, 0.08753900000000003, 0.22475099999999998, 0.09633000000000001, 0.19442900000000002, 0.4359, 0.26321799999999995, 0.25533100000000003, 0.22823000000000004, 0.166388, 0.25262799999999996, 0.4109, 0.2486, 0.18297500000000003, 0.110846, 0.20582599999999998, 0.22857399999999994, 0.46775, 0.19116700000000006, 0.43095, 0.38155, 0.4215, 0.39135, 0.22331199999999993, 0.35845000000000005, 0.37415357142857136, 0.20354499999999998, 0.25, 0.17454299999999998, 0.47635, 0.3612, 0.3506, 0.38675, 0.12150899999999992, 0.19974600000000003, 0.14704000000000003, 0.186099, 0.218541, 0.42115, 0.3506, 0.302089, 0.4078, 0.3612, 0.12261900000000002, 0.200222, 0.18150300000000008, 0.30946799999999985, 0.12601700000000005, 0.21882899999999997, 0.19745199999999993, 0.17253100000000018, 0.17413699999999996, 0.216517, 0.33594999999999997, 0.18900100000000003, 0.29929300000000003, 0.181348, 0.015986000000000004]

dfsp = pd.read_json('stockprice.json')
#print(dfsp['Change %'])
price_changes = dfsp['Change %'].to_numpy()
#print(price_changes)
def f(x):
  #print(x)
  xsize = len(x)
  for index in range(0,xsize):
    xwsize = len(x[index])-1
    x[index]=float(x[index][0:xwsize])
  
  return x

pc = f(price_changes)
pct_change_res = []
rd_size = len(results_daily)
print(rd_size)
for i in range(0,(rd_size)):
  num1 = results_daily[i]
  if num1==0:
    num1 = 0.01
  pct_change_res.append(num1)

pc=np.array(pc).reshape(1,-1)
pct_change_res=np.array(pct_change_res).reshape(1,-1).astype(float)
#print(len(pct_change_res))

npscopy1 = np.copy(pc)
npsortcopy1 = np.sort(npscopy1)
#print(npsortcopy)
npsortcopy21 = np.flip(npsortcopy1)
newmin = npsortcopy1[0][1]
newmax = npsortcopy21[0][1]
print((newmin))
print((newmax))
diff = (newmax-newmin)
print(diff)
pc = pc * (100 /diff)

#print(pct_change_res)
#print("b+bmax")
#print(b+bmax)

npscopy = np.copy(pct_change_res)
npsortcopy = np.sort(npscopy)
#print(npsortcopy)
npsortcopy2 = np.flip(npsortcopy)
newmin = npsortcopy[0][1]
newmax = npsortcopy2[0][1]
#print((newmin))
#print((newmax))
diff = (newmax-newmin)
#print(diff)
pct_change_res = pct_change_res * (100 /diff)
#print(pct_change_res)
#print(pct_change_res)
#print(pc)
pc=pc.astype(float)
pct_change_res = pct_change_res[0][:505]
print("len below")
print(len(pct_change_res))
slope, intercept, r_value, p_value, std_err = sp.linregress(pc[0], pct_change_res)
print(r_value**2)
print(p_value)
print(slope)
#plt.plot(pct_change_res, pc[:505], 'o')

from scipy.signal import savgol_filter
dys = []
for i in range (1, 506):
  dys.append(i)
#print(pc)
#normalized regresss here
pc = pc.flatten()
pc = np.array(pc)
pct_change_res = pct_change_res.flatten()
pct_change_res1 = savgol_filter(pct_change_res, 5, 2)
pc1 = savgol_filter(pc, 3, 2)
slope1, intercept1, r_value1, p_value1, std_err1 = sp.linregress(pc1, pct_change_res1)
print(p_value1)
print(r_value1)
print(std_err)
plt.plot(dys, pct_change_res1, dys, pc1)
axes = plt.gca()
x_vals = np.array(axes.get_xlim())
y_vals = intercept + slope * x_vals
#plt.plot(x_vals, y_vals, 'b')