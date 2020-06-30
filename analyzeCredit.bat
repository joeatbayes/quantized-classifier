::rm classifyFiles.exe
::go build src/classifyFiles.go
classifyFiles -train=data/credit.train.csv -test=data/credit.test.csv -minBuck=2 -maxBuck=10 -testout=tmpout/credit.test.out.csv -detToStdOut=false -catColumns=A1,A4,A5,A6,A7,A8,A9,A10,A12,A13,A14,A11,A15 -IgnoreColumns=tclass -doPreAnalyze=true -AnalClassId=0  -AnalTestPort=100 -AnalAdjFeatWeight=true -model=tmpout/credit.model.csv 

::A2,A3,A8,A16 are treated as numeric by default