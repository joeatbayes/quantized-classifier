::go build src/classifyFiles.go
classifyFiles -train=data/wine.data.usi.train.csv  -test=data/wine.data.usi.test.csv -maxBuck=10 -testout=tmpout/wine.tst.out.csv  -doOpt=false -optrandomize=false -optMaxTime=1.5
