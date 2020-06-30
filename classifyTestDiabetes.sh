#!/bin/sh
export GOPATH=$PWD
#rm classifyFiles.exe
#go build src/classifyFiles.go
classifyFiles -train=data/diabetes.train.csv -test=data/diabetes.test.csv  -minBuck=5 -maxBuck=10 -testOut=tmpout/diabetes.test.csv  
::50