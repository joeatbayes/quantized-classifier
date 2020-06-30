::rm classifyFiles.exe
::go build src/classifyFiles.go
classifyFiles -train=data/titanic.train.csv -test=data/titanic.test.csv -minBuck=10 -maxBuck=400 -testout=tmpout/Titanic.test.out.csv -detToStdOut=false  -doPreAnalyze=true -AnalClassId=1  -AnalTestPort=100 -AnalAdjFeatWeight=true -model=tmpout/titanic.model.det.csv
:600