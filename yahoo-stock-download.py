# Documentation https://code.google.com/p/yahoo-finance-managed/wiki/csvHistQuotesDownload
# updated for python 3.5
# Months are 0..11
#
# NOTE:  AS OF Aug-3-2017 Yahoo data is no longer available for free
#   http://eoddata.com offers historical data for a reasonable price.
#   See also: convert_EODDate_hist_to_bars.py
#
# NOTE:  As of Jan-1-2018 Google Download API appears to have been
#  cut off.   The only cheap source I currently know of is supplied 
#  by http://eoddata.com/products/historicaldata.aspx but it's large
#  downside is that the data may not be republished which makes 
#  use for opensource projects problematic.   
#
#  Please let me know if you find good sources for bar data free
#  to download and republish.  
#
#  See also: https://www.quantshare.com/sa-43-10-ways-to-download-historical-stock-quotes-data-for-free
#  See also: https://www.barchart.com/ondemand/free-market-data-api


import http.client

def fetchYahoo(symbol, begYear, begMonth, begDay,  endYear, endMonth, endDay):
  uri = "/table.csv?s=" + symbol + "&d=" + str(endMonth) + "&e=" + str(endDay) + "&f=" + str(endYear) + "&g=d&a=" + str(begMonth) + "&b=" + str(begDay) + "&c=" + str(begYear) + "&ignore=.csv"
  print ("uri=",  uri)
  conn = http.client.HTTPConnection("ichart.finance.yahoo.com")
  conn.request("GET", uri)
  r1 = conn.getresponse()
  data1 = r1.read()
  print (data1)
  fname = "data/" + symbol + ".csv"

  tarr = data1.decode().strip().split("\n")
  head = tarr[0]
  body = tarr[1:]
  body.reverse()
  body.insert(0,head)
  f = open(fname, "w")
  f.write("\n".join(body))
  f.close()
  return data1
  
print ("""
  NOTE:  JOE E: I tested this on Aug-3-2017 and found that")
  Yahoo has discontinued their free data service
  An alternative source of data is http://EODData.com
  """)
  
#           symbol begin     End
#fetchYahoo("SPY",  2010,0,1, 2017,2,10)
#fetchYahoo("SLV",  2007,0,1, 2017,2,10)
#fetchYahoo("GLD",  2005,0,1, 2017,2,10)
#fetchYahoo("CAT",   2004,0,1, 2017,2,10)
#fetchYahoo("IBM",  2005,0,1, 2017,2,10)
