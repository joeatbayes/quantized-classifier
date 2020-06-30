export GOPATH=$PWD
classifyFiles -train=data/diabetes.train.csv -test=data/diabetes.test.csv -maxBuck=700 -testOut=tmpout/diabetes.test.csv  -detToStdOut=false -doPreAnalyze=true -AnalSplitType=1 AnalTestPort=0.1  -AnalClassId=1
