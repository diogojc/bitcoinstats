import pandas as pd
from pandas import Series, DataFrame
from math import ceil
from numpy import arange
import matplotlib
import matplotlib.pyplot as plt

# load data into timeseries
df = DataFrame.from_csv("hist/BTC.csv")
df["time"] = pd.to_datetime(df["time"], unit='s')
ts = Series(data=df["close"].values, index=df["time"])

# calculate returns after investing
dataset = DataFrame()
maxdays = (ts.index[-1]-ts.index[0]).days
for n in range(1, maxdays):
    chg = ts.pct_change(n)
    chg = chg[chg.notnull()]
    tmp = DataFrame({'x': chg.values*0+n, 'y': 1+chg.values})
    dataset = dataset.append(tmp)
average = dataset.groupby(['x']).mean()

# setup plotting
matplotlib.rcParams['agg.path.chunksize'] = 1000

# plot returns over time
plt.figure()
plt.yscale('log', basey=2)
plt.xlabel('Years invested in bitcoin')
plt.ylabel('Cash multiplier')
plt.title('Returns after investing')
nrYears = ceil(dataset.index.max()/365)+1
plt.xticks(arange(0, nrYears)*365, arange(0, nrYears))
plt.grid(linestyle='dashed')
plt.plot(dataset['x'], dataset['y'],
         marker=",", alpha=0.3, linestyle="None", color="green")
plt.plot(average, color="black")
plt.savefig("returns.png", dpi=600)

# plot loss probability over time
plt.figure()
plt.xlabel('Years invested in bitcoin')
plt.ylabel('Chance of loss')
plt.title('Chance of losing in bitcoin')
plt.grid(linestyle='dashed')
count = dataset.groupby('x').count()
lossCount = dataset[dataset.y < 1].groupby('x').count()
lossProb = count.copy()
lossProb.y = 0
lossProb.ix[lossCount.index] = lossCount.y/count.ix[lossCount.index].y
plt.xticks(arange(0, nrYears)*365, arange(0, nrYears))
plt.plot(lossProb.index, lossProb.values)
plt.savefig("lossprob.png", dpi=600)
