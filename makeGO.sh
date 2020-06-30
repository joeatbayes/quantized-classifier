#!/bin/sh
export GOPATH=$PWD

go build src/splitCSVFile.go
go build src/classifyTest.go
go build src/csvInfoTest.go
go build src/classifyFiles.go

