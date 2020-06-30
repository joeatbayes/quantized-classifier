# create_rate_return_columns.py
#
# Create a % rate of return for each of symbols in the listed directory.
#
# By Joe Ellsworth 2017-08-20 See license.txt
# Inspired by: http://cs229.stanford.edu/proj2013/TakeuchiLee-ApplyingDeepLearningToEnhanceMomentumTradingStrategiesInStocks.pdf
# Applying Deep Learning to Enhance Momentum Trading Strategies in Stocks
# Lawrence Takeuchi * ltakeuch@stanford.edu Yu-Ying (Albert) Lee yy.albert.lee@gmail.com
#

from datetime import datetime,  timedelta
import time
import datetime

def readFile(inFiName):
  toutarr = []
  toutbydate = {}
  with open(inFiName) as f:
      header = f.readline()
      for line in f:
          line = line.strip()
          #print("line=", line)
          arr = line.split(",")
          symbol = arr[0]
          datestr = arr[1]
          date = datetime.datetime(*time.strptime(datestr, "%Y-%m-%d")[:6])
          popen = float(arr[2])
          pclose = float(arr[3])
          phigh = float(arr[4])
          plow = float(arr[5])
          vol  = long(arr[6])
          ele = (symbol, date, popen, pclose, phigh, plow, vol, [])
          toutarr.append(ele)
          toutbydate[date] = len(toutarr)
      return toutarr, toutbydate
    

# Easiest way to comput Rate of return is to ignore the
# actual dates and simply compute the rate of return based
# on Number of bars previous knowing that on average each month
# has 22 bars.   A more accurate way is to subtract the number
# of days to equal exactly one month earlier.   To get the basic
# algorithm working we will use the # of bars.
def computeRateOfReturn(days, byDates, rorReq):
  ndx = 0
  #print "L46: rorReq=", rorReq
  for symbol, date, popen, pclose, phigh, plow, vol, returnArr in days:
    for tele in rorReq:
      # print "L49: tele=", tele
      daysBack, numDays = tele
      maxDays = daysBack + numDays
      endNdx = ndx - daysBack
      startNdx = ndx - maxDays
      ror = -1
      if startNdx < 0:
        ror = -99
      else:
        bsymbol, bdate, bopen, bclose, bhigh, blow, bvol, brr = days[startNdx]
        xsymbol, xdate, xopen, xclose, xhigh, xlow, xvol, xrr = days[endNdx]
        if bopen == 0.0:
          ror = -2
        else: 
          pchange = xclose - bopen
          # https://en.wikipedia.org/wiki/Rate_of_return
          ror = round((pchange / bopen),5)
          #print "pchange=", pchange, "ror=", ror
      returnArr.append(ror);
      
    #print "L68: ", symbol, date, returnArr
    ndx = ndx + 1
    
def saveComputedROR(outDir, bars, rorReq):
  symbol = bars[0][0]
  outFiName = outDir + "/" + symbol + ".csv"
  print "outFiName=", outFiName
  with open(outFiName, "w") as outFile:
    # Compute new header based on look back ROR period
    header = ["symbol","date","open","close","high","low","volume"]
    for daysBack, numDays in rorReq:
      header.append( "R" + str(daysBack) + "_" + str(numDays))
    headStr = ",".join(header) + "\n"
    outFile.write(headStr)

    for symbol, date, popen, pclose, phigh, plow, vol, returnArr in bars:
      outarr = [symbol, str(date), str(popen), str(pclose), str(phigh), str(plow), str(vol)]
      for aror in returnArr:
        outarr.append(str(aror))
      outline = ",".join(outarr) + "\n"
      outFile.write(outline)
    

def processFile(inFiName, outDir, rorReq):
  print ("fiName=", inFiName)
  days, byDates = readFile(inFiName)
  print ("numDays=", len(days))
  computeRateOfReturn(days, byDates, rorReq)
  saveComputedROR(outDir, days, rorReq)
  


def processDir(globPath, outDir, rorReq):
  import glob
  print "L102: rorReq=", rorReq
  flist =  glob.glob(globPath)
  flist.sort(); # process oldest dates first assuming
    # the file names are generated to produce correct
    # ordering using string compare of file name.
  print("numFiles=", len(flist), flist[0])
  for fiName in flist:
    processFile(fiName, outDir, rorReq)
    
# Compute Rate of Return for a date started back from current bar
# second # is number of days to include in the ror
ROR = [(0,22), (23,22), (44,22), (66,22),(88,22),(110,22),(132,22),(154,22),(176,22),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1)]

processDir("../../../JTDATA/eoddata/nyse/gen/*.csv",
           "../../../JTDATA/eoddata/nyse/rate-return-01", ROR)

