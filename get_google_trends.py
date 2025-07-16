from pytrends.request import TrendReq

pytrends = TrendReq()

kw_list = ["Apple"]
pytrends.build_payload(kw_list, timeframe='today 3-m')

data = pytrends.interest_over_time()

if not data.empty:
    print(data.tail())
else:
    print("No trend data found.")

