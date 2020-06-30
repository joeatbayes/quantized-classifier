::rm classifyFiles.exe
::go build src/classifyFiles.go
classifyFiles -train=data/diabetes.train.csv -test=data/diabetes.test.csv -minBuck=3 -maxBuck=15 -testOut=tmpout/diabetes.test.csv  
::60