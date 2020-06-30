# stock-prep-sma.py
# Convert simple time series stock data into something
# we can possibly use for machine learning classification
# 
# Convert a stock bar file into a tagged stock 
# data more interesting for machine learning.
# The rule will be that the price from a given Bar
# measured as day open must rise by X% before it 
# drops by Y%.  If it does then that bar is classified
# as 1.  Those that fall by more than X% are classified
# as a 0.  
#
# Four our indicators we are going to use a series of
# SMA and compute the slope of the line from the SMA
# for current bar to sma at some bars in the past. 

import math

def strx(aNum):
  return "{:0.3f}".format(aNum)

# TODO:  Need to Audit the SMA ouptut   
def sma(vect, numAvgBar):
  rowCnt = 0
  divNum = 0
  runTot = 0
  tout = []
  for anum in vect:
    if (rowCnt >= (numAvgBar)):
      runTot -= vect[rowCnt - numAvgBar]
    rowCnt += 1
    divNum = min(rowCnt, numAvgBar)
    runTot += anum
    avg = runTot / divNum
    tout.append(avg)
  return tout
  
    
def ratioAboveMin(vect, curNdx, maxLookback):
  ndx = curNdx
  begndx = max(0,curNdx - maxLookback)
  minVal = vect[curNdx]
  currVal = vect[curNdx]
  minNdx = curNdx
  while ndx >= begndx:
    if vect[ndx] < minVal:
      minNdx = ndx
      minVal = vect[ndx]
    ndx -= 1
  ndxDelt = curNdx - minNdx
  valDif = currVal - minVal
  ratio = valDif / minVal
  return ratio, ndxDelt

def ratioBelowMax(vect, curNdx, maxLookback):
  ndx = curNdx
  begndx = max(0,curNdx - maxLookback)
  maxVal = vect[curNdx]
  currVal = vect[curNdx]
  maxNdx = curNdx
  while ndx >= begndx:
    if vect[ndx] > maxVal:
      maxNdx = ndx
      maxVal = vect[ndx]
    ndx -= 1
  ndxDelt = curNdx - maxNdx
  valDif = maxVal - currVal
  ratio = valDif / maxVal
  return ratio, ndxDelt
    

def slopeAboveMin(vect, curndx, maxLookback):
  rat, age = ratioAboveMin(vect, curndx, maxLookback)
  if age == 0:
    return 0
  return (rat / age) * 10000

def slopeBelowMax(vect, curndx, maxLookback):
  rat, age = ratioBelowMax(vect, curndx, maxLookback)
  if age == 0:
    return 0
  return (rat / age) * 10000


def slope(currNdx, vectSrc, vectCmp, barsPast):
  begNdx = max(0, currNdx - barsPast)
  currVal = vectSrc[currNdx]
  oldVal  = vectCmp[begNdx]
  dif = currVal - oldVal
  slope = ((dif / oldVal) / barsPast) * 10000
  return slope


# If we had purchased on this bar would we have made money
# before our stop loss exited the trade.
# return true if price rises by at least goalRisep as portion
# of current close before it drops below goaldropp as portion
# of current close.   Otherwise return 0  
def findClassRiseBeforeFall(currNdx, maxHold, goalRisep, goalDropp, oClose, oHigh, oLow):
  maxNdx = len(oClose)
  cout = 0
  currClose = oClose[currNdx]
  goalRiseAmt = currClose * goalRisep
  endTargRiseAmt = goalRiseAmt * 0.5
  endTargSucc = currClose + endTargRiseAmt
  maxPrice  = currClose + (currClose * goalRisep)
  minPrice  = currClose - (currClose * goalDropp)
  holdBars = 0
  for ndx in range(currNdx+1, maxNdx):    
    if oHigh[ndx] > maxPrice:
      return 1, holdBars  # sucess 
    if oLow[ndx] < minPrice:
      return 0, holdBars # failed 
    
    # If have held for too long then 
    # consider sucess if price has risen
    # by more than 1/2 of goal
    if holdBars > maxHold:
      if oClose[ndx] > endTargSucc:
        return 1,holdBars
      elif oClose[ndx] > currClose:
        return 2, holdBars # It rose but not by much
      elif oClose[ndx] > minPrice:
        return 3, holdBars
      else:
        return 0, holdBars
    holdBars += 1        
  return 0, holdBars

  

  
class Transformer:

  def __init__(self, inName, outName, symbol):
    self.inName = inName
    self.outName = outName
    self.symbol = symbol
    self.outTrainName = outName.replace(".csv", ".train.csv")
    self.outTestName  = outName.replace(".csv", ".test.csv")
    self.outClassName = self.outTrainName.replace(".train.", ".class.")
    self.date  = []
    self.close = []
    self.low   = []
    self.high  = []
    self.open  = []
    self.portSetTrain = 0.80
    self.loadData(inName)
    self.numBar = len(self.open)
    
    
    print("portion of set for Training=", self.portSetTrain)
    print ("trainName=", self.outTrainName, " testName=", self.outTestName)  


   
  def loadData(self,fiName):
     oDate  = self.date
     oClose = self.close
     oLow   = self.low
     oHigh  = self.high
     oOpen  = self.open
     with open(fiName, 'r') as fi:
       rows = fi.readlines()[1:]
       for aline in rows:      
        row = aline.split(",")
        bartime = row[0]
        close = float(row[4])
        low   = float(row[3])
        high  = float(row[2])
        topen = float(row[1])
        oDate.append(bartime)
        oClose.append(close)
        oLow.append(low)
        oHigh.append(high)
        oOpen.append(topen)       
       
  def savePortSet(self, fiName, begNdx, endNdx, srcVect, cmpVect, classVect):
      with open(fiName, "w") as fout:
        fout.write("class,symbol,datetime,sl3,sl6,sl12,sl20,sl30,sl60,sl90,sbm10,sbm20,sam10,sam20,ram20,ram30,rbm10,rbm20,sam90,sam180,sam360,sbm90,sbm180,sbm360\n")
        oDateTime = self.date
        
        for ndx in range(begNdx,endNdx):
          slope1 = slope(ndx,srcVect,cmpVect,3)
          slope2 = slope(ndx,srcVect,cmpVect,6)
          slope3 = slope(ndx,srcVect,cmpVect,12)
          slope4 = slope(ndx,srcVect,cmpVect,20)
          slope5 = slope(ndx,srcVect,cmpVect,30)
          slope6 = slope(ndx,srcVect,cmpVect,60)
          slope7 = slope(ndx,srcVect,cmpVect,90)
          sam6   = slopeAboveMin(srcVect, ndx, 6)
          sam10   = slopeAboveMin(srcVect, ndx, 10)
          sam90   = slopeAboveMin(srcVect, ndx, 90)
          sam180   = slopeAboveMin(srcVect, ndx, 180)
          sam360   = slopeAboveMin(srcVect, ndx, 360)
          sam20   = slopeAboveMin(srcVect, ndx, 20)
          sbm6    = slopeBelowMax(srcVect, ndx, 6)
          sbm10   = slopeBelowMax(srcVect, ndx, 10)
          sbm20   = slopeBelowMax(srcVect, ndx, 20)
          sbm90   = slopeBelowMax(srcVect, ndx, 90)
          sbm180   = slopeBelowMax(srcVect, ndx, 180)
          sbm360   = slopeBelowMax(srcVect, ndx, 360)
          ram6,xx  = ratioAboveMin(srcVect, ndx, 10)
          ram10,xx  = ratioAboveMin(srcVect, ndx, 10)
          ram20,xx  = ratioAboveMin(srcVect, ndx, 20)
          ram30,xx  = ratioAboveMin(srcVect, ndx, 30)
          rbm6,xx  = ratioBelowMax(srcVect, ndx, 10)
          rbm10,xx  = ratioBelowMax(srcVect, ndx, 10)
          rbm20,xx  = ratioBelowMax(srcVect, ndx, 20)
          rbm30,xx  = ratioBelowMax(srcVect, ndx, 30)
          
          bclass = classVect[ndx]          
          tout = [str(bclass),self.symbol,oDateTime[ndx],strx(slope1),strx(slope2),strx(slope3),
                  strx(slope4),strx(slope5),strx(slope6), strx(slope7),                
                  strx(sbm10),strx(sbm20),
                  strx(sam10),strx(sam20),
                  strx(ram20),strx(ram30),
                  strx(rbm10),strx(rbm20),
                  strx(sam90),strx(sam180), strx(sam360),
                  strx(sbm90),strx(sbm180), strx(sbm360)]
          ts = ",".join(tout)
          #print("ndx=",ndx, "s=", ts)
          fout.write(ts)
          fout.write("\n")

  def getSrcCmpVect(self,cmpx,smaLen):
    srcVect = self.close
    if cmpx == "high":
      cmpVect = self.high
    elif cmpx == "low":
      cmpVect = self.low
    elif cmpx == "open":
      cmpVect = self.open
    elif cmpx == "smahigh":
      cmpVect = sma(self.high, smaLen)
    elif cmpx == "smaclose":
      cmpVect = sma(self.close, smaLen)
    elif cmpx == "smaopen":
      cmpVect = sma(self.open, smaLen)
    elif cmpx == "smalow":
      cmpVect = sma(self.low, smaLen)    
    else:
      cmpVect = self.close
    return srcVect, cmpVect

  def processRiseBeforeFall(self,maxHold, amtRise, amtFall, smaLen, cmp):
    
    print("inName=", self.inName)
    srcVect, cmpVect = self.getSrcCmpVect(cmp, smaLen)
    print("smaLen=", smaLen)
    numBar = self.numBar
    numTrainRow = int((self.numBar - smaLen) *  self.portSetTrain)

    # Save with our original rise before fall
    # logic for classification
    classVect = []
    for ndx in range(0, numBar):
      tclass, holdTime = findClassRiseBeforeFall(ndx, maxHold, amtRise, amtFall, self.close, self.high, self.low)
      classVect.append(tclass)
      
    self.savePortSet(self.outTrainName, smaLen+1, smaLen + numTrainRow,srcVect,cmpVect,classVect)
    self.savePortSet(self.outTestName,  smaLen+numTrainRow+1, numBar, srcVect,cmpVect,classVect)     
    self.savePortSet(self.outClassName, numBar-5, numBar, srcVect, cmpVect,classVect)


  # Find a class for a given bar based on a Hold For
  # X time.  If Gain is >= minGainRatio then class = 1
  # if loss > 0 - minGainRatio then return class = 2
  # else return class = 0  
  def findClassHoldN(self, currNdx, holdFor, minGainRatio, startVect, cmpVect):
    endNdx = min((currNdx + holdFor), (self.numBar - 1))
    cout = 0
    currPrice = startVect[currNdx]    
    cmpPrice = cmpVect[endNdx]
    priceChange = cmpPrice - currPrice
    priceChangeRatio = priceChange / currPrice
    if priceChangeRatio > minGainRatio:
      return 1
    elif priceChangeRatio < (0 - minGainRatio):
      return 3
    elif priceChange < 0.0:
      return 2
    else:
      return 0
    
    #classId = 1000 + int(priceChange / stepSize)    
    #return classId


  def processHoldForN(self,holdFor, minGainRatio, smaLen, cmpx):
    ## Now Save with Alternate Classify strategy
    ## of holding for fixed period of time classifying
    ## by price change.
    srcVect, cmpVect = self.getSrcCmpVect(cmpx, smaLen)
    numBar = self.numBar
    numTrainRow = int((self.numBar - smaLen) *  self.portSetTrain)
    classVect = []
    for ndx in range(0, numBar):
      tclass = self.findClassHoldN(ndx, holdFor, minGainRatio, self.close, self.open)
      classVect.append(tclass)
      
    self.savePortSet(self.outTrainName, smaLen+1, smaLen + numTrainRow,srcVect,cmpVect,classVect)
    self.savePortSet(self.outTestName,  smaLen+numTrainRow+1, numBar, srcVect,cmpVect,classVect)     
    self.savePortSet(self.outClassName, numBar-5, numBar, srcVect, cmpVect,classVect)
    



def procRiseBeforeFall(inFiName, outFiName, symbol, maxHold, amtRise, amtFall, smaLen, cmpx):
  pcs =   Transformer(inFiName, outFiName, symbol)
  pcs.processRiseBeforeFall(maxHold, amtRise, amtFall, smaLen, cmpx)

def procHoldForN(inFiName, outFiName, symbol, holdFor, minGainRatio, smaLen,cmpx):
  pcs =   Transformer(inFiName, outFiName, symbol)
  pcs.processHoldForN(holdFor, minGainRatio, smaLen, cmpx)
  

def genRiseBeforeFall():

  # TODO:  Modify to support same day exit.  Entrance is based on Open so buy when price condition 
  #    is good and Min drops below open then sell when Max rises above the threashold assume we
  #    will not set a stop limit on exit.  Would be better with 1 minut bars.

  procRiseBeforeFall("data/spy.csv", "data/spy-8up-4dn-mh90-close.csv", "spy", 90, 0.080, 0.04,2,"close")  # 2 to 1 gain ratio
  procRiseBeforeFall("data/spy.csv", "data/spy-1p0up-0p5dn-mh4-close.csv", "spy", 4, 0.010, 0.005,30,"close")  # 2 to 1 gain ratio
  procRiseBeforeFall("data/spy.csv", "data/spy-2p2up1-1dn-mh6-close.csv", "spy", 6, 0.022, 0.01,30,"close")  # 220% gain ratio
  procRiseBeforeFall("data/spy.csv", "data/spy-6up-1dn-mh10-smahigh90.csv","spy", 10, 0.06,  0.01,90,"smahigh") # 6 to 1 gain ratio

  procRiseBeforeFall("data/cat.csv", "data/cat-7p8up1p2dn-mh5-close.csv", "cat", 5, 0.078, 0.012,50,"close") # 6.41667 to 1 gain ratio
  procRiseBeforeFall("data/cat.csv", "data/cat-1p7up1p2dn-mh2-close.csv", "cat", 2, 0.017, 0.012,10,"close") # 1.4167 to 1 gain ratio

  procRiseBeforeFall("data/cat.csv", "data/cat-6up-1dn-mh45-smahigh90.csv","cat", 45, 0.06,  0.01,90,"smahigh") # 6 to 1 gain ratio

  #process("data/spy.csv", "data/spy-1up-1dn-mh5-low.csv","spy", 5, 0.01, 0.01,30,"low") # 1 to 1 gain ratio
  #process("data/spy.csv", "data/spy-1up-1dn-mh5-open.csv","spy", 5,0.01, 0.01,30,"open") # 1 to 1 gain ratio 
  #process("data/spy.csv", "data/spy-1up-1dn-mh5-high.csv","spy", 5,0.01, 0.01,30,"high") # 1 to 1 gain ratio on high
  #process("data/spy.csv","data-spy-1up-1dn-mh5-smaclose30.csv", "spy", 5 0.01, 0.01,30,"smaclose") # 1 to 1 gain ratio

  # Seek silver bars that rise more than 1.5% before
  # falling by 0.3%  This represents a 5X profit
  # compared to losses so a sucess rate above 0.2
  # is adequate. 
  procRiseBeforeFall("data/slv.csv", "data/slv-1p5up-0p3dn-mh10-close.csv", "slv", 5, 0.015, 0.003,30,"close")

def genHoldForN():

  procHoldForN("data/spy.csv", "data/spy-hold-005-close.csv",  "spy", 5, 0.01, 0,"close")
  procHoldForN("data/spy.csv", "data/spy-hold-015-close.csv", "spy", 15,  0.02, 0,"close")
  procHoldForN("data/spy.csv", "data/spy-hold-030-close.csv", "spy", 30,  0.03, 0,"close")
  procHoldForN("data/spy.csv", "data/spy-hold-060-close.csv", "spy", 60,  0.04, 0,"close")
  procHoldForN("data/spy.csv", "data/spy-hold-090-close.csv", "spy", 90,  0.05, 0,"close")
  procHoldForN("data/spy.csv", "data/spy-hold-180-close.csv", "spy", 180, 0.05,0,"close")
  procHoldForN("data/gld.csv", "data/gld-hold-005-close.csv", "gld", 5, 0.01, 0,"close")
  procHoldForN("data/gld.csv", "data/gld-hold-015-close.csv", "gld", 15,  0.02, 0,"close")
  procHoldForN("data/gld.csv", "data/gld-hold-030-close.csv", "gld", 30,  0.03, 0,"close")
  procHoldForN("data/gld.csv", "data/gld-hold-060-close.csv", "gld", 60,  0.04, 0,"close")
  procHoldForN("data/gld.csv", "data/gld-hold-090-close.csv", "gld", 90,  0.05, 0,"close")
  procHoldForN("data/gld.csv", "data/gld-hold-180-close.csv", "gld", 180, 0.05,0,"close")

genRiseBeforeFall()
#genHoldForN()

