::rm classifyFiles.exe
::go build src/classifyFiles.go
classifyFiles -train=data/titanic.train.csv -test=data/titanic.test.csv -minBuck=7 -maxBuck=365 -testout=tmpout/Titanic.test.out.csv
