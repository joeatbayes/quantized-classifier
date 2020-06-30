export GOPATH=$PWD
classifyFiles -train=data/titanic.train.csv -test=data/titanic.test.csv -maxBuck=250 -testout=tmpout/Titanic.test.out.csv -detToStdOut=false  -doPreAnalyze=true -AnalSplitType=1 -AnalClassId=1  -AnalTestPort=0.1
