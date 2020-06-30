""" Convert Cifar data into something
  we can read as a standard CSV File
  in the classifier.

  Runs in python 3.5 will not work with python 2.7

  Data was downloaded from http://www.cs.toronto.edu/~kriz/cifar.html
  CIFAR-10 python version http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz

  I copied the unzipped data to one directory
  above my managed git-hub repository because
  I didn't want to accidentally check in files
  that large.

  Processing the downloaded file
    gzip -d cifar-10-python.tar.gz
    tar -xvf cifar-10-python.tar
    
"""

def unpickle(file):
    import _pickle as cPickle
    fo = open(file, 'rb')
    dict = cPickle.load(fo, encoding="bytes")
    fo.close()
    return dict

def convertToCSV(inFiName, outStream, genLabel):
  tdict = unpickle(inFiName)
  rowndx = 0
  data = tdict[b'data']
  labels = tdict[b'labels']
  fiNames = tdict[b'filenames']
  numCol = len(data[0])
  totCol = numCol + 1
  if genLabel == True:
    clabels = [0] * totCol
    print("numCol=", numCol)
    print("clables=", clabels)
    clabels[0] = "class"
    for cndx in range(1, totCol):
      clabels[cndx] = "c" + str(cndx)
    labelstr = ",".join(clabels) + "\n"
    outStream.write(labelstr)
  # Process the data rows 
  outrow = [0] * totCol 
  for arow in data:
    label = labels[rowndx] 
    rowndx += 1
    outrow[0] = str(label)
    cndx = 1
    for colval in arow:
      #print("cndx=", cndx, "colval=", colval)
      outrow[cndx] = str(colval)
      cndx += 1
    tstr = ','.join(outrow) + "\n"
    outStream.write(tstr)

""" Read all the input files converting them
to CSV output. Only the first file needs a
header output all the others will are written
into the same output.
"""
def processInFiles(inFiNames, outFiName):
  fiCnt = 0
  outStream = open(outFiName, "w")
  processLabels = True
  for fiName in inFiNames:
    convertToCSV(fiName, outStream, processLabels)
    processLabels = False
  outStream.close()
    
trainFiles = ["../cifar-10-batches-py/data_batch_1",
              "../cifar-10-batches-py/data_batch_2",
              "../cifar-10-batches-py/data_batch_3",
              "../cifar-10-batches-py/data_batch_4",
              "../cifar-10-batches-py/data_batch_5",
              ]

processInFiles(trainFiles, "cifar-10.train.csv")

processInFiles(["../cifar-10-batches-py/test_batch"], "cifar-10.test.csv")
  
