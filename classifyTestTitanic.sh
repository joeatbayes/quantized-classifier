#!/bin/sh
export GOPATH=$PWD
#rm classifyFiles.exe
#go build src/classifyFiles.go
classifyFiles -train=data/titanic.train.csv -test=data/titanic.test.csv -minBuck=5 -maxBuck=565 -testout=tmpout/Titanic.test.out.csv
