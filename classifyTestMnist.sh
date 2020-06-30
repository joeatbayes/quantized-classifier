#!/bin/sh
export GOPATH=$PWD
#rm classifyFiles.exe
#go build src/classifyFiles.go
classifyFiles -train=data/mnist.train.csv -test=data/mnist.test.csv -numBuck=155 -testout=tmpout/Mnist.test.csv
