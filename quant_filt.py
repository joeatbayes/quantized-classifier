""" Simple gesture classification using quantized filter. 

    Tested with Python 3.52
    Please use with Python 3.5 or greater.  It produces erroneous results when using python 2.7
    
    WARN: Example Only intended to demonstrate principals
    of quantized filter algorithm.  Production version will be
    implemented in src/qprob as a GO library.

    Eg: The AT Feature has the following discrete values 
    1.0, 0.79, 0.505, 0.47, 0.70, 0.40, 0.08  We quantize the values 
    into discrete buckets for feature 1.   For each of these buckets we 
    we create list of buckets for feature 2.  For each of these buckets we 
    create a list of buckets for feature 4 until we run out of features. 
    
    This data structure was inspired by splay search trees 
    
    This allows a very fast lookup filter so only those records that have a 
    matching filter all the way down the tree survive.  When we have very large
    training sets with limited noise this can be a very fast and powerful algorithm.
    At the termal bucket for the last feature we keep the list of classes with a counter
    of the number of examples that were placed in that bucket. 
    
    The system builds the underlying data structure 
    maxBuckets from 2 to GBLMaxNumBuck -1 and returns 
    the list of matches for each level of max buckets.  
    In general a smaller number of buckets will increase 
    recall while a larger number of buckets will increase 
    precision.  If you get a match with a relatively high 
    number of buckets such as 8 or 9 then it is a pretty 
    high quality confidence. 

    Tree[bucketId][bucketId][bucketId][bucketId]... = { containing counts by class }
    If you get a result returning more than one class then the highest probability
    match is for the class with the highest count assuming random distribution of noise
    in the training data.
    

  TODO:  The BuckId calculation is incorrect
   because we need to know the effective range 
   of data values before we can compute a bucket
   size.   The version here will work but it requires
   all values to be converted into a value between
   zero and 1 and even then it would not effectively
   handle outliers.    
 
 """
  

import csv
import sys
import json
import random
import sys
assert sys.version_info >= (3,5)
 # Tested with Python 3.52 and 3.62
 #  Produces erroneous results when using python 2.7
 

class QuantTreeFilt:
  def __init__(self, inFiName, classCol, minNumBuck, maxNumBuck):
    #self.colVals = []
    self.inFiName = inFiName
    # InFiName is used mostly to load the list of
    # field names from CSV.  It is normally the training
    # file but in the future may also represent the
    # model file.
    
    self.trees =  self.trees = [dict() for x in range(maxNumBuck)]
    self.numCol = 0 # read as part of csv head
    #self.numClass = 0
    self.rowCnt = 0 # number of rows read in training set
    self.maxNumBuck = maxNumBuck # Increase num buckets for max precision reduce for max recall
    self.classCol = classCol
    self.maxByCol = [] # list of max values read by column
    self.minByCol = [] # list of min values read by column
    self.absRange = [] # list of abs range for values in column
    self.stepSizeByCol = [] # list of step sizes computed by col
    self.header = []  # List of field names read from CSV
    
    self.minNumBuck = minNumBuck # Set this to at least 2 if you don't
                        # want a wild guess on some rows.  When
                        # set to 1 it will force a answer for
                        # every row.
                        
    self.headStr = ""
    self.colByPos = []
    self.colNames = {}
    self.readColNames(inFiName)

    self.maxNumBuckByCol = [] # Created this to allow minimum / maximum # buckets to change by feature
    self.minNumbuckByCol = [] # Created this to allow minimum / maximum # buckets to change by feature
    for aval in self.colByPos:
      self.maxNumBuckByCol.append(maxNumBuck) # Created this to allow minimum / maximum # buckets to change by feature
      self.minNumbuckByCol.append(minNumBuck) # Created this to allow minimum / maximum # buckets to change by feature
  
    
    

  def getBuckId(self, colNum, numBuck, sval):
      
     dval = 0
     try:
       dval = float(sval)
     except ValueError:
       # If can not convert to a float number
       # then just return the input value this
       # allows string values to be indexed as
       # unique buckets
       return sval

    
     if numBuck == 1:
       return 0

      
     absRange = self.absRange[colNum]
     stepSize =  absRange / (numBuck)
     minval = self.minByCol[colNum]
     if dval == minval:
       return 0
     amtOverMin = dval - minval
     numStep = amtOverMin / stepSize
     buckId = int(numStep)
     if numBuck == 1 and buckId != 0:
       print("L112: colNum=", colNum, "dval=", dval, " sval=", sval, "minVal=", minval,  "numBuck=", numBuck,"stepSize=", stepSize, "amtOverMin=",
            amtOverMin, " numStep=", numStep, " absRange=", absRange, " buckId=", buckId)
     # Note: BuckId will be negative when dval
     # is less than minValue encountered during
     # training
     return buckId
     
    
  # Updates stats in tree form from
  # 1 bucket through self.maxNumBuck
  def updateStats(self, arow, numBuck, fieldList):        
    classCol = self.classCol
    trees = self.trees
    rclass = int(arow[classCol])    
    
    # Initialize our current buck to
    # starting point in our tree.
    currBuck = trees[numBuck]

    # Build a nested Tree containing
    # one layer per feature
    for mfn, ndx in enumerate(fieldList):
      colVal = arow[ndx]
      if ndx != classCol:        
        buckId = self.getBuckId(ndx, numBuck, colVal)
        if not buckId in currBuck:
          # If bucket does not exist then
          # we need a new one to track this value
          #print("L100: Create new Bucket id=", buckId)
          currBuck[buckId] = {}  
        currBuck = currBuck[buckId]  
        #print("L143: numBuck=", numBuck, " buckId=", buckId, "rclass=", rclass, "currBuck=", currBuck)
        
    # Finished walking the bucket tree 
    # to reach sentinal value for the number
    # of Columns Now record count by class  
    if not rclass in currBuck:
      currBuck[rclass] = 1
    else:
      currBuck[rclass] += 1
    # Keep a Total Count for all classes 
    # at this level so we can compute a 
    # Base probability
    if not "t" in currBuck:
      currBuck["t"] = 1
    else:
      currBuck["t"] += 1

  def parseColNames(self, aStr):
    tout = {}
    tarr = aStr.split(",")
    ndx = 0
    for cname in tarr:
      cname = cname.strip().lower()
      tout[cname] = ndx
      ndx += 1
    return tout
  
                              
  def readColNames(self, fiName):
    with open(fiName, 'r') as csvfile:
      self.headStr = csvfile.readline()
      self.colByPos = self.headStr.split(",")
      self.colNames = self.parseColNames(self.headStr)
      return self.colNames
      
               
  def readTrainingData(self, fiName,  fieldList):
    minNumBuck = self.minNumBuck
    maxNumBuck = self.maxNumBuck
    with open(fiName, 'r') as csvfile:
      rreader = csv.reader(csvfile, dialect='excel', delimiter=',', quotechar='"')
      rowCnt = 0
      for row in rreader:    
        if rowCnt == 0:
          header = row
        else:
          for nb in range(minNumBuck, maxNumBuck):
            self.updateStats(row, nb, fieldList)
        rowCnt += 1                                  
                      

  # Match a list of fieldnames up to available column names
  # Return an array of column numbers for all columns that
  # do not match                               
  def fieldsPosMinusSkipNames(self, fieldNames):
      tout = []
      #print ("L197: self.colNames=", self.colNames)
      skips = self.parseColNames(fieldNames)
      #print("L199: skips=", skips)
      for akey  in self.colNames:
        val = self.colNames[akey]
        #print("L199: akey=", akey, " val=", val)
        if not (akey in skips):
          tout.append(val)
      #print("L204: tout=", tout)
      tout.sort()
      return tout
                              
  

  # Match a list of fieldnames up to available column names
  # return a list of column numbers that match 
  def matchFieldNames(self, fieldNames):
      tout = []
      fields = self.parseColNames(fieldNames)
      for akey, val in enumerate(fields):
        if akey in self.colNames:
          tout.append(val)
      tout.sort()      
      return tout
                              
        
  def readMinMax(self, fiName):
    classCol = self.classCol
    maxNumBuck = self.maxNumBuck
    minNumBuck = self.minNumBuck
    numCol = self.numCol
    print("L236: readMinMax minNumBuck=", minNumBuck, "maxNumBuck=", maxNumBuck, "numCol=", numCol)
    
    with open(fiName, 'r') as csvfile:
      rreader = csv.reader(csvfile, dialect='excel', delimiter=',', quotechar='"')
      rowCnt = 0
      numCol = 0
      for row in rreader:    
        if rowCnt == 0:
          # Reading the header row so we initialize
          # a bunch of instance variables based on
          # how many features we detected. 
          self.header = row
          numCol = len(row)
          self.numCol = numCol
          # Initialize array to hold min/max
          # values 
          self.maxByCol =  [-99999999999.0] * numCol
          self.minByCol =  [999999999999.0] * numCol
          self.absRange = [0] * numCol
          self.stepSizeByCol = [0] * numCol
          self.colVals = [dict() for x in range(numCol)]
         
                 
        else:
          # Reading a real row 
          for nb in range(minNumBuck, maxNumBuck):
            for ndx, dval in enumerate(row, start=0):
              fval = 0
              try:
                fval = float(dval)
              except ValueError:
                continue
              if fval > self.maxByCol[ndx]:
                self.maxByCol[ndx] = fval
              elif fval < self.minByCol[ndx]:
                self.minByCol[ndx] = fval                        
        rowCnt += 1
      self.numRow   = rowCnt

      # Now compute the actual abs range by column
      # used to compute step size latter. 
      for ndx, maxVal in enumerate(self.maxByCol , start=0):        
        self.absRange[ndx] = maxVal - self.minByCol[ndx]

      #print("L192: self.minByCol=",self.minByCol)
      #print("L193: self.maxByCol=",self.maxByCol)
      #print("L194: self.absRange=", self.absRange)
      
        
      
  def matchNumBuck(self, drow, numBuck, matchFields): 
    classCol = self.classCol    
    rclass =  drow[classCol]
    colndx = 0
    currBuck = self.trees[numBuck]
    #print("L218: matchNumBuck() numBuck=", numBuck, "matchFields=", matchFields,  "currBuck=", currBuck)
    for mfn, ndx in enumerate(matchFields):
      fval = drow[ndx]
      if ndx != classCol:        
        buckId = self.getBuckId(ndx, numBuck, fval)
        #print ("L223 ndx=", ndx, "fval=", fval, " buckId=", buckId)
        if not buckId in currBuck:
          #print("L225 fail ndx=", ndx, " fval=", fval, " buckId=", buckId, "numBuck=", numBuck, " currBuck=", currBuck)
          return None
        else:
          currBuck = currBuck[buckId]
          #print ("L229: buckId=", buckId, " currBuck=", currBuck)
    #print("L230: currBuck=", currBuck)
    return currBuck # This is the count by classId
  
         
  # Since the most precise trees will end up returning
  # none when there is no match we compute the probability
  # based on less granular.  This higher the number of 
  # buckets where we find a match the better the quality of our
  # match. 
  def match(self, features, matchFields):
    tout = {}
    for nb in range(self.minNumBuck, self.maxNumBuck):      
      twrk = self.matchNumBuck(features, nb, matchFields)
      tout[nb] = twrk
      #print("L242: nb=", nb, " twrk=", twrk)
    return tout
    

  ## TODO:  Think about a match where we walk the tree 
  ##  using the maximum number of buckets where we find 
  ##  a match for each feature.  If we can not find a match
  ##  For that item then we walk back to the next most 
  ##  reduced item for that feature.  EG: In some features
  ##  We want to use 8 buckets for others we may need to 
  ##  use 2 buckets that means we have to detect failure 
  ##  at a given point and backtrack until we find a match
  ##  but once back tracked we have to walk forward from there

  # Determine quality of match 
  def chooseRowResult(self, rowRes):                            
     currNdx = -999999999
     currRow = None
     for ndx in rowRes:
       #print("L261: ndx=", ndx)
       fval = rowRes[ndx]
       #print ("L263: ndx=", ndx, " fval=", fval)
       if fval != None and ndx > currNdx: 
           # Match with the highest ndx will 
           # be the most specific match 
           currNdx = ndx
           currRow = fval
     #print("L269: currNdx=", currNdx, "currRow=", currRow)
     return currNdx, currRow     
      
  def readTestData(self, fiName, matchFields):
    classCol = self.classCol
    tout = []
    with open(fiName, 'r') as csvfile:
      rreader = csv.reader(csvfile, dialect='excel', delimiter=',', quotechar='"')
      rowCnt = 0
      for row in rreader:    
        if rowCnt == 0:
          testHeader = row      
        else:
          actClassId = int(row[classCol])
          #print("L283 row=", row)
          # Reading data values
          matchRes = self.match(row, matchFields)
          #print("L286: matchRes=", matchRes)
          level, choice = self.chooseRowResult(matchRes)
          
          # TODO: Move This section Out to separate Method
          # Interpret results 
          #print("L266: level=", level, " choice=", choice)
          bestClass = None
          bestClassCnt = 0
          if choice == None:
            #print("L279: No choice for row ", rowCnt, " row=", row)
            tout.append({"act" : actClassId, "stat" : "fail",
                         "reason" : "noMatch", 
                         "row=" : row})
            continue
          #print("L301: choice=", choice)
          totCnt = choice["t"]
          
          # Find our Best Class out of choices
          # at this level and create prob by
          # class for each results
          trec = {}
          trec["tot"] = totCnt
          for cid in choice:
            if cid == "t":
              continue            
            cnt = choice[cid]            
            #print("L281: cid=", cid, " cnt=", cnt, "totCnt=", totCnt)         
            prob = cnt / totCnt
            cObj = { "cnt" : cid, "prob" : prob }
            trec[cid] = cObj            
            if cnt > bestClassCnt:
              bestClassCnt = cnt
              bestClass = cid
          trec["best"] = bestClass
          trec[bestClass]["best"] = True
          trec["act"] = actClassId
          trec["lev"] = level
          #print("L294: trec=", trec)
          
          # Record whether our best match
          # coincides with our actual class
          if bestClass == actClassId:                                    
            trec["stat"] = "ok"
          else:
            trec["stat"] = "fail"                               
          tout.append(trec)
        rowCnt += 1
    return tout

def makeEmptyClassSum(id):
  return {"id" : id, "totCnt" : 0, "sucCnt" : 0, "noClass" : 0,
          "taggedCnt" : 0,  "precis" : 0.0, "recall" : 0.0}


def analyzeTestRes(res):  
  rrecs = []
  totCnt = 0
  sucCnt = 0
  failRateCnt = 0
  byClass = {}
  tout = { "byClass" : byClass, "NoClass" : 0 }
  
  for rrow in res:
    totCnt += 1
    stat = rrow["stat"]
    actClass  = rrow["act"]
        
    if not actClass in byClass:
      byClass[actClass] =  makeEmptyClassSum(actClass)
    byClass[actClass]["totCnt"] += 1

    if not "best" in rrow:
      tout["NoClass"] += 1
      rrecs.append(rrow)
      byClass[actClass]["noClass"] += 1
      continue
    
    cid = rrow["best"]
    if not cid in byClass:
      byClass[cid] =  makeEmptyClassSum(cid)      
    tagClass = byClass[cid]
    tagClass["taggedCnt"] += 1
    
    if stat == "ok":
      sucCnt += 1
      tagClass["sucCnt"] += 1
      
    prob = rrow[cid]["prob"]
    trow = [cid, prob, actClass, stat]
    rrecs.append(trow)

  tout["NumRow"] = totCnt
  tout["NumPred"] = totCnt - tout["NoClass"]
  if tout["NumPred"] > 0:
    prec = sucCnt / tout["NumPred"]
  else:
    prec = 0
  tout["SucessCnt"] = sucCnt
  tout["FailCnt"] = tout["NumPred"] - sucCnt 
  tout["Precision"] = prec  
  tout["NoClassRate"] = tout["NoClass"] / totCnt
  tout["TotRecall"] = (totCnt - tout["NoClass"]) / totCnt
  
  for classId in byClass:
    aclass = byClass[classId]
    aclass["fail"] = aclass["taggedCnt"] - aclass["sucCnt"]
    aclass["classProb"] = aclass["totCnt"] / totCnt
    try:
      aclass["precis"] = aclass["sucCnt"] / aclass["taggedCnt"]
    except ZeroDivisionError:
      aclass["precis"] = -1

    try:
      aclass["recall"] = aclass["sucCnt"] / aclass["totCnt"]
    except ZeroDivisionError:
      aclass["recall"]
      
  return tout, rrecs
    

def resScore(analyzedRes, targClass):
  if not "byClass" in analyzedRes:
    return -2
  byClass = analyzedRes["byClass"]
  if not targClass in byClass:
    return -1
  tclass = byClass[targClass]
  #print("L477 tclass=", tclass)
  valAdj = 1.0
  if tclass["taggedCnt"] < 2:
    valAdj = 0.1
  elif tclass["recall"] < 0.05:
    valAdj = 0.2
  elif tclass["recall"] < 0.10:
    valAdj = 0.5   
  return (tclass["precis"] * 1.9 + tclass["recall"] + analyzedRes["Precision"] * 0.05 + analyzedRes["TotRecall"] * 0.03) * valAdj

  
        
def processFieldList(trainFiName, testFiName, minNumBuck, maxNumBuck, targetClass, fieldList):
  #print("L468: trainFiName=", trainFiName, " testFiName=", testFiName, "targetClass=", targetClass,  "maxNumBuck=", maxNumBuck)
  qf =  QuantTreeFilt(trainFiName, 0, minNumBuck,  maxNumBuck)
  qf.readMinMax(trainFiName)

  #print("L476: fieldList=", fieldList)   
  qf.readTrainingData(trainFiName, fieldList)
  tout = qf.readTestData(testFiName, fieldList)
  #print (" tout=", tout)

  analyzedRes, recs = analyzeTestRes(tout)
  
  
  #print ("\n\nAnalyzed recs=", recs)
  #print ("\n\n\nAnalyzed\n", json.dumps(analyzedRes, sort_keys=True, indent=3))
  return analyzedRes, recs
  


def permutateFields(trainFiName, testFiName, minNumBuck, maxNumBuck, targetClass, skipFields):
  # In our optimization process we need to optimize
  # based on our training data set we can not look at the
  # test data set until we are all done. 
  print("L468: permutateFields() trainFiName=", trainFiName, " testFiName=", testFiName, "targetClass=", targetClass,  "maxNumBuck=", maxNumBuck)
  qf =  QuantTreeFilt(trainFiName, 0, minNumBuck,maxNumBuck)
  qf.readMinMax(trainFiName)

  fieldList = qf.colByPos
  firstScore = -1
  if skipFields != None:
    fieldList = qf.fieldsPosMinusSkipNames(skipFields)
    analyzedRes, recs = processFieldList(trainFiName, trainFiName, minNumBuck, maxNumBuck, targetClass, fieldList)
    firstScore = resScore(analyzedRes, targetClass)
  print ("L520: firstScore=", firstScore)


  # Find Best Column to start from the set of available columns.
  bestScore = -99
  bestFld  = None
  print("L508: fieldList=", fieldList, " skipFields=", skipFields)
  tlist = []
  for fndx in fieldList:
    tmpFldLst = [fndx]
    analyzedRes, recs = processFieldList(trainFiName, trainFiName, minNumBuck, maxNumBuck, targetClass, tmpFldLst)
    ascore = resScore(analyzedRes, targetClass)
    tlist.append((ascore, fndx, analyzedRes))
    if ascore > bestScore:
      bestScore = ascore
      bestCol = fndx
    print("L524: fndx=", fndx, " ascore=", ascore, " bestScore=", bestScore, "bestCol=", bestCol)
  tlist.sort()
  tlist.reverse()
  #print("L527: Sorted by Field Quality", json.dumps(tlist, sort_keys=True, indent=3))

  # Now try adding our best columns to the list of colums we are using
  # one by one to see if they improve the score.
  wrkList = [bestCol]
  for tpl in tlist:
    score, ndx, rec = tpl
    if not (ndx in wrkList):
      wrkList.append(ndx)
      analyzedRes, recs = processFieldList(trainFiName, trainFiName, minNumBuck, maxNumBuck, targetClass, wrkList)
      ascore = resScore(analyzedRes, targetClass)
      print("L538: ndx=", ndx, "ascore=", ascore, " Best Score=", bestScore)
      if ascore >= bestScore:
        bestScore = ascore        
      else:
        print("L544: do not keep ndx", ndx)
        wrkList.pop() # remove the last item because it did not help
      #print("L541: fndx=", fndx, " ascore=", ascore, " bestScore=", bestScore, "bestCol=", bestCol)
  print("L545 chosen Set")
  analyzedRes, recs = processFieldList(trainFiName, testFiName, minNumBuck, maxNumBuck, targetClass, wrkList)
  ascore = resScore(analyzedRes, targetClass)
  print("L547: ndx=", ndx, "ascore=", ascore, " Best Score=", bestScore)
  print("L548: Final List=", wrkList)  
  #print ("L550: Analyzedn", json.dumps(analyzedRes, sort_keys=True, indent=3))

  if firstScore > bestScore:
    print("L565: First Score was better using it as starting point")
    bestScore = firstScore
    wrkList = fieldList

  # If the first try with the full set of fields yields a better
  # result then use it otherwise use the list developed from
  # first list. 
  # Now Try start with the initial full set of available fields
  wrkListKey = ','.join(str(e) for e in wrkList)
  featSetTried = {wrkListKey : ascore }
  tryCnt = 0
  choiceTypes = [0,1,2] # 0 = delete field, 1 = add field, 2 = add,delete
  # randomly add and remove columns to see if we can improve
  # the score. 
  while tryCnt < 500:
    tryCnt += 1
    featNotUsed = []
    for fldNdx in fieldList:
      if not (fldNdx in wrkList):
        featNotUsed.append(fldNdx)
      numNotUsed = len(featNotUsed)
      
    # Choose fields to try
    newFldNdx = -1
    if len(featNotUsed) > 0:
      newFldNdx = random.choice(featNotUsed)
      
    delFldNdx = random.choice(wrkList)
    newWorkList = []
    choice = random.choice(choiceTypes)
    
    # Remove a random column
    for aval in wrkList:
      if aval != delFldNdx or choice == 1:
        newWorkList.append(aval)
    # Add a random column
    if (choice == 1 or choice == 2) and (newFldNdx != -1):
      newWorkList.append(newFldNdx)
    if len(newWorkList) < 1:
      newWorkList.append(random.choice(fieldList))
    newWorkList.sort()  
    wrkListKey = ','.join(str(e) for e in newWorkList)
    #print("L582: tryCnt=", tryCnt, "delNdx=", delFldNdx, " addNdx=", newFldNdx, "newWorkList=", newWorkList, " wrkListKey=", wrkListKey)
    if   wrkListKey in  featSetTried:
      #print ("L585: Already tried wrkListKey=", wrkListKey)
      pass
    else :
      analyzedRes, recs = processFieldList(trainFiName, trainFiName, minNumBuck, maxNumBuck, targetClass, newWorkList)
      ascore = resScore(analyzedRes, targetClass)
      featSetTried[wrkListKey] = ascore
        
      #print("L587: ndx=", ndx, "ascore=", ascore, " Best Score=", bestScore)
      if ascore >= bestScore:
        bestScore = ascore
        wrkList = newWorkList # Keep the changes
        print("L591: Keep: wrkListKey=", wrkListKey, "ascore=", ascore, " bestScore=", bestScore)
      else:
        print("L593: Reject wrkList=", wrkListKey, "ascore=", ascore, " bestScore", bestScore)
        # Naturally reverse if we do not save the changes      
      #print("L596: fndx=", fndx, " ascore=", ascore, " bestScore=", bestScore, "bestCol=", bestCol)

  # Test it with our actual test data set.
  analyzedRes, recs = processFieldList(trainFiName, testFiName, minNumBuck, maxNumBuck, targetClass, wrkList)
  ascore = resScore(analyzedRes, targetClass)      
  print("L606: Final field list=", wrkList, " ascore=", ascore, "analyzedRes=",  json.dumps(analyzedRes, sort_keys=True, indent=3))  



              
      
def processTest(trainFiName, testFiName, minNumBuck, maxNumBuck, targClass, skipFields):
  print("L646: trainFiName=", trainFiName, " testFiName=", testFiName, " minNumBuck=", minNumBuck, " maxNumBuck=", maxNumBuck, "targclass=", targClass, "skipfields=", skipFields)
  qf =  QuantTreeFilt(trainFiName, 0, minNumBuck, maxNumBuck)
  qf.readMinMax(trainFiName)

  fieldList = qf.colByPos
  if skipFields != None:
    fieldList = qf.fieldsPosMinusSkipNames(skipFields)
    print("L544: fieldList=", fieldList)   
     
  print("L546: fieldList=", fieldList)   
  qf.readTrainingData(trainFiName,fieldList)
  tout = qf.readTestData(testFiName, fieldList)
  #print (" tout=", tout)

  analyzedRes, recs = analyzeTestRes(tout)
  
  print("trainFiName=", trainFiName, " testFiName=", testFiName, " maxNumBuck=", maxNumBuck)
  #print ("\n\nAnalyzed recs=",)
  #print (recs)
  print ("\n\n\nAnalyzed\n")
  print(json.dumps(analyzedRes, sort_keys=True, indent=3))

  print ("\n\n\nPERMUTATE\n\n\n")
  permutateFields(trainFiName, testFiName, minNumBuck, maxNumBuck, targClass, skipFields)


# Question: How much benefit if we add MinNumBuck to
#   Reduce the time of execution and control how far back
#   the generalized lookups are allowed to go. 
# 
# Question:  Could we support a custom number of buckets
#   by feature.   If so how much risk of over learning
#   do we introduce. 
   
## ---- 
## -- MAIN
## ----

# Increase num buckets for max precision reduce for max recall

#processTest('data/gest/gest_train_ratio2.csv', 'data/gest/gest_test_ratio2.csv', GBLMaxNumBuck)

#processTest('data/breast-cancer-wisconsin.adj.data.train.csv', 'data/breast-cancer-wisconsin.adj.data.test.csv', 7,11,4,"")

#processTest('data/diabetes.train.csv', 'data/diabetes.test.csv', 8,21, 1, "")

#processTest('data/liver-disorder.train.csv', 'data/liver-disorder.test.csv', 11,15, 1, "")

#processTest('data/wine.data.usi.train.csv', 'data/wine.data.usi.test.csv', 11,15, 2, "")

#processTest('data/titanic.train.csv', 'data/titanic.test.csv', 10,19, 1, "")


#####
### CAT
#####
#processTest('data/cat-1p7up1p2dn-mh2-close.train.csv', 'data/cat-1p7up1p2dn-mh2-close.test.csv', 13,15,1, "class,symbol,datetime")
#processTest('data/cat-6up-1dn-mh45-smahigh90.train.csv', 'data/cat-6up-1dn-mh45-smahigh90.test.csv', 14,17,1, "class,symbol,datetime")
#processTest('data/cat-7p8up1p2dn-mh5-close.train.csv', 'data/cat-7p8up1p2dn-mh5-close.test.csv', 13,19,1, "class,symbol,datetime")

#####
## SILVER 
#####
processTest('data/slv-1p5up-0p3dn-mh10-close.train.csv', 'data/slv-1p5up-0p3dn-mh10-close.test.csv', 12,18,1, "class,symbol,datetime")
#processTest('data/slv-1p5up-0p3dn-mh10-close.train.csv', 'data/slv-1p5up-0p3dn-mh10-close.test.csv', 13,17,1, "class,symbol,datetime")


########
#### SPY
########
#processTest('data/spy-8up-4dn-mh90-close.train.csv', 'data/spy-8up-4dn-mh90-close.test.csv', 9,11, 1, "class,symbol,datetime")
#processTest('data/spy-2p2up1-1dn-mh6-close.train.csv', 'data/spy-2p2up1-1dn-mh6-close.test.csv', 9,11, 1, "class,symbol,datetime")
#processTest('data/spy-1p0up-0p5dn-mh4-close.train.csv', 'data/spy-1p0up-0p5dn-mh4-close.test.csv', 9,11, 1, "class,symbol,datetime")
#processTest('data/spy-6up-1dn-mh10-smahigh90.train.csv', 'data/spy-6up-1dn-mh10-smahigh90.test.csv', 5,11, 1, "class,symbol,datetime" )


#processTest('BodyStateModel-paper_train.csv', 'BodyStateModel-paper_test.csv', 8, 10, "")

