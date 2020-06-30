::go build src/classifyFiles.go
classifyFiles -train=data/breast-cancer-wisconsin.adj.data.train.csv -test=data/breast-cancer-wisconsin.adj.data.test.csv -minBuck=2 -maxBuck=11 -WriteJSON=false  -testOut=tmpout/breast-cancer.test.out.csv  
