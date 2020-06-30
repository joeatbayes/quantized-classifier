::rm classifyFiles.exe
::go build src/classifyFiles.go
classifyFiles -train=data/liver-disorder.test.csv -test=data/liver-disorder.train.csv -maxBuck=500 -testout=tmpout/liver-disorder.test.csv -detToStdOut=false  -doPreAnalyze=true -AnalTestPort=100 -AnalAdjFeatWeight=false  -model=tmpout/liverDisorder.model.det.csv

