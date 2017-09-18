import urllib
import json
from pandas import DataFrame

coinListUrl = "https://www.cryptocompare.com/api/data/coinlist/"
response = urllib.urlopen(coinListUrl)
coinList = json.loads(response.read())["Data"]
i = .0
for k in coinList:
    coinHistUrl = "https://min-api.cryptocompare.com/data/histoday?fsym=%s&tsym=EUR&allData=true" % k
    try:
        response2 = urllib.urlopen(coinHistUrl)
        response2Data = json.loads(response2.read())["Data"]
        if response2Data is not None and len(response2Data) > 0:
            coinHist = DataFrame(response2Data)
            coinHist.to_csv("hist/%s.csv" % k)
            print "[%.2f%%] Saved %s.\n" % (i/len(coinList)*100, k)
    except Exception:
        print "[%.2f%%] Failed to save %s.\n" % (i/len(coinList)*100, k)
    i += 1
