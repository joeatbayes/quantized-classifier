from __future__ import print_function
""" CNNClassify.py  A multi layered Neural Network
 classifier implemented using tflearn and and
 TensorFlow.  It can read and classify any of the
 CSV filles suppored by our go utility ClassifyFiles
 which implements a Quantized probability classifer.

 The results for the test cases is the quantized 
 classifer is faster and produces slightly more 
 accurate results but if you crank the epoch 
 on the convoluted NN to 30 it will sometimes
 beat the quantized classifer but it takes about
 20 times as long to train in that mode. 
"""
import numpy as np
import tflearn
import sys
import os
import json


# In TFLearn class labels are used to 
# create a array of potential outputs
# the class ID must be integers 
# and we need to know how many there
# will be before we use the tflear reader.
def getNumClass(fiName, colNum):
  f = open(fiName)
  lines = f.readlines()[1:]
  f.close()
  maxClass = -989999999
  labVals = []
  for line in lines:
    flds = line.split(",")
    try:
      aclass = int(flds[colNum])
      if aclass >= maxClass:
        maxClass = aclass + 1
    except ValueError:
      aclass = -99999
    labVals.append(aclass)
  return maxClass, labVals

# Locate the best anser in the prediction
# array and return the classId and computed
# prob for that answer. classId start
def best(arr):
  bestP = 0
  bestNdx = -1
  currNdx = 0
  for val in arr:
    if val > bestP:
      bestP = val
      bestNdx = currNdx
    currNdx += 1
  return bestP, bestNdx
    
   
 
def load(fiName):
  numClass, labVal = getNumClass(fiName, 0)
  print("numClass=", numClass)
  # Load CSV file, indicate that the first column represents labels
  from tflearn.data_utils import load_csv
  data, labels = load_csv(fiName,
      target_column=0, categorical_labels=True, n_classes=numClass)

  # Map Convert the number string input into
  # numerics.
  numRow = len(data)
  numCol = len(data[0])
  for rndx in range(0, numRow):
    for cndx in range(0, numCol):
      try:
        data[rndx][cndx] = float(data[rndx][cndx])
      except ValueError:
         data[rndx][cndx] = -9999.0
      
  data = np.array(data, dtype=np.float32)

  #print("data as float array=", data)
  #print("labels=", labels)
  numCol = len(data[0])
  numRow = len(data)
  return (numRow, numCol, numClass, data, labels, labVal)
  

def run(trainFiName, testFiName, n_epoch):
  numRow, numCol, numClass, data, labels, labVal = load(trainFiName)
  tstNumRow, tstNumCol, tstNumClass, tstData, tstLabels, tstLabVal = load(testFiName)

  print("numCol=",numCol, "numRow=", numRow, " numClass=", numClass)

  # Build neural network
  net = tflearn.input_data(shape=[None, numCol])
  net = tflearn.fully_connected(net, 32)
  net = tflearn.fully_connected(net, 32)
  net = tflearn.fully_connected(net, numClass, activation='softmax')
  net = tflearn.regression(net)

  # Define model
  model = tflearn.DNN(net)
  # Start training (apply gradient descent algorithm)
  model.fit(data, labels, n_epoch=n_epoch, batch_size=55, show_metric=True)

 
  

  def printSimpRes(pred):
    # Run the prediction for the 
    # Test data set  

    rowndx = 0
    sucessCnt = 0
    for rowp in pred:
      bestP, classId = best(rowp)
      actPred = tstLabVal[rowndx]
      labelStr = "fail"
      if actPred == classId:
        labelStr = "success"
        sucessCnt += 1      
      print("class=", classId, " prob=", bestP, " ", labelStr)
      rowndx += 1
    sucPerc = (sucessCnt / tstNumRow) * 100
    failPerc = 100.0 - sucPerc
    print("tested=", tstNumRow, "suceed=", sucessCnt, "good%=", sucPerc, 
          " fail=", tstNumRow - sucessCnt, " failPerc=", failPerc)
  



  def analyzeTestRes(res):  
    rrecs = []
    totCnt = 0
    sucCnt = 0
    failRateCnt = 0
    byClass = {}
    tout = { "byClass" : byClass, "NoClass" : 0 }

    rowndx = 0
    for rrow in res:
      totCnt += 1
      stat = "ok"
      
      prob, classId = best(rrow)
      actClass = tstLabVal[rowndx]
      if not actClass == classId:
        stat = "fail"
      
      if not actClass in byClass:
        byClass[actClass] =  makeEmptyClassSum(actClass)
      byClass[actClass]["totCnt"] += 1

      
      cid = classId 
      if not cid in byClass:
        byClass[cid] =  makeEmptyClassSum(cid)      
      tagClass = byClass[cid]
      tagClass["taggedCnt"] += 1
      
      if stat == "ok":
        sucCnt += 1
        tagClass["sucCnt"] += 1
        
     
      trow = [cid, prob, actClass, stat]
      rrecs.append(trow)
      rowndx +=1

    tout["NumRow"] = totCnt
    tout["NumPred"] = totCnt 
    prec = sucCnt / tout["NumPred"] 
    tout["SucessCnt"] = sucCnt
    tout["FailCnt"] = tout["NumPred"] - sucCnt 
    tout["Precision"] = prec  
    tout["TotRecall"] = totCnt  / totCnt
    
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

      
  pred = model.predict(tstData)
  printSimpRes(pred)
  tout, rrecs = analyzeTestRes(pred)
  print ("\n\n\nAnalyzed\n", json.dumps(tout, sort_keys=True, indent=3))

      

def help():
  print("usage CNNClassify.py trainFileName testFiName num_epoch")
  print("argv=", str(sys.argv))
  raise SystemExit

def makeEmptyClassSum(id):
  return {"id" : id, "totCnt" : 0, "sucCnt" : 0, "noClass" : 0,
          "taggedCnt" : 0,  "precis" : 0.0, "recall" : 0.0}



 
if len(sys.argv) != 4:
  print("incorrect number of command line args")
  help()
trainFiName = sys.argv[1]
testFiName = sys.argv[2]
n_epoch = int(sys.argv[3])

if os.path.isfile(trainFiName) == False:
  print("train file does not exist ", trainFiName)
  help()
  
if os.path.isfile(testFiName) == False:
  print("test file does not exist", testFiName)
  help()
 
print ("CNNClassify.py trainFiName=", trainFiName, " testFiName=", testFiName, " n_epoch=", n_epoch)
run(trainFiName, testFiName, n_epoch)
    
#run('../data/breast-cancer-wisconsin.adj.data.train.csv', '../data/breast-cancer-wisconsin.adj.data.test.csv')

#run('../data/diabetes.train.csv', '../data/diabetes.test.csv')




