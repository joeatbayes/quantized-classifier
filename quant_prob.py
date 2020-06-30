"""
 OBSOLETE - This example is only intended to show the 
   quantized probability model in a simple piece of code.
   the production version is implemented in src/qprob/classify.go
   
 Simple_gest_quant_prob - For the basic gesture descriptions

   Adds basic probabilistic measure of individual bucket membership
   to allows ensemble style combination of results. 

    Eg: The AT Feature has the following discrete values 
    1.0, 0.79, 0.505, 0.47, 0.70, 0.40, 0.08  We quantize the values 
    into discrete buckets and that are fast to compute and lookup. To match
    we compute the bucket id for each feature then keep a counter for the 
    class ids that were referenced. Larger sample sets give us a larger number
    of buckets to accomodate variations.

   
  produces colVals[1..NumFeat]
     Each ColVal = {} Indexed by bucketId
       Each classId = {} Indexed RClass 
         colVals[columnNumber][BucketId][classId] = CountOfRowsMatching
         colVals[columnNumber][BucketId]["tot"]   = CountOfAllRowsInBucket
 
 """
  

import csv
import sys
assert sys.version_info >= (3,5)
 # Tested with Python 3.52 and 3.62
 #  Produces erroneous results when using python 2.7
 

colVals = []
features = {}
numFeat = 0
numClass = 0
rowCnt = 0 # number of rows read in training set
GBLNumBuck = 5
classCnt = {} # Count of all records for a given class
probInClass = {} # probability of a given record being in a each class
probNotInClass = {} # probabilty of given record not being in each class


# For each feature for each quant available
#  in that feature record the count of occurances
#  for each class.
def updateStats(arow):
  rclass = int(arow[0])
  if not rclass in classCnt:
    classCnt[rclass] = 0
  classCnt[rclass] += 1
  rest = arow[1:]
  colndx = 0;
  for colVal in rest:
    buckId = int(float(colVal) * GBLNumBuck)
    acol = colVals[colndx]
    if not buckId in acol:
     acol[buckId] = { 'tot' : 0 }
    aBuckSet = acol[buckId]    
    if not rclass in aBuckSet:
     aBuckSet[rclass] = 0
    aBuckSet[rclass] += 1
    aBuckSet["tot"] += 1
    colndx += 1
    
    
# Compute probability of any given row being a member
# and probability of not being a member of a given class.
# Need for Baysean probability latter. 
def updateProbInClass():
  for classId in classCnt:
    aCnt = classCnt[classId]
    probInClass[classId] = aCnt / rowCnt
    probNotInClass[classId] = rowCnt - aCnt / rowCnt
    

def readTrainingData(fiName):
  global numFeat, colVals, rowCnt
  with open(fiName, 'r') as csvfile:
    rreader = csv.reader(csvfile, dialect='excel', delimiter=',', quotechar='"')
    rowCnt = 0
    for row in rreader:    
      if rowCnt == 0:
        header = row
        numFeat = len(row)- 1
        colVals = [dict() for x in range(numFeat)]        
      else:
        updateStats(row)
      rowCnt += 1
    updateProbInClass()

# When matching we find the best quantized match for each
# item then compute a probability of match for each class
# we keep these probabilities to combine in the next step
# to obtain an ensemble.
def match(features): 
  colndx = 0
  detProb = {}
  totCnt = 0
  #  Compute the probability for each feature being in 
  #  of a given class by feature the combine those 
  #  probabilties.  That way we will give higher priority
  #  to buckets that contain fewer records belonging to
  #  another class.  See Actual Bayesian prob which includes
  #  probability of not being in the class.
  #
  # Update the count for matching bucket
  for fval in features:
    buckId = int(float(fval) * GBLNumBuck)
    acol = colVals[colndx]
    if buckId in acol:
      aBuckSet = acol[buckId]
      buckTotCnt = aBuckSet['tot']
      for classId in aBuckSet:
        if classId == "tot":
          continue
        featBuckCnt= aBuckSet[classId]
        totCnt += 1
        if not classId in detProb:
          detProb[classId] = []
        #TODO: Adust this to be actual Bayesean Prob
        classProb = (featBuckCnt / buckTotCnt) * probInClass[classId]
        detProb[classId].append(classProb)
    colndx += 1
    

  # Assemble total probability from features
  # as a sum of the individual feature probability
  # acting like an ensemble.
  prob = {}
  bestClass = None
  bestProb   = 0
  for classId in detProb:
    totProb = 0.0
    cntProbs = detProb[classId]
    for aProb in cntProbs:
      totProb = (totProb + aProb) 
    prob[classId] = totProb;
    if totProb > bestProb:
      bestClass = classId
      bestProb = totProb

  return { 'best' :  {"class" : bestClass, "prob" : bestProb },
           'detProbs=' : detProb, 'classProbs=' : prob }
  
    
## ---- 
## -- MAIN
## ----
readTrainingData('data/train/gest_train_ratio2.csv')
print("colVals=", colVals)

 
matchHSamp =  match([0.082,0.14,0.924,1.000,0.602,0.885])


print ("matchHSamp = ", matchHSamp)


matchYSamp =  match([0.242,0.120,0.154,0.305,0.730,0.745])
print ("mathYSamp = ", matchYSamp)
