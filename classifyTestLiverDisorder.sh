#!/bin/sh
export GOPATH=$PWD
#rm classifyFiles.exe
#go build src/classifyFiles.go
classifyFiles -train=data/liver-disorder.test.csv -test=data/liver-disorder.train.csv -maxBuck=20 -testout=tmpout/liver-disorder.test.csv 

