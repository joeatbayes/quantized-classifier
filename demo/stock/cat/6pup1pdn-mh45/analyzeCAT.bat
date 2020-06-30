::rm classifyFiles.exe
::go build src/classifyFiles.go
::
::
:: To Run the Stock example on SPY data first run the 
:: the utility to download data from yahoo python yahoo-stock-download.py
:: then run utility to convert raw stock data into machine learning
::  data python stock-prep-sma.py then  you can run
:: this module.

:: Seeking a 6% Rise at profit taker before a 
::  1% loss at stop loss with max hold of 45 
::  days.


set XXCWD=%cd%
cd ..\..\..\..\

classifyFiles -train=data/cat-6up-1dn-mh45-smahigh90.train.csv -test=data/cat-6up-1dn-mh45-smahigh90.test.csv -testOut=tmpout/cat-6up-1dn-mh45-smahigh90.out.csv  -model=tmpout/cat-6up-1dn-mh45-smahigh90.model.csv  -minBuck=490 -maxBuck=500 -detToStdOut=false -doPreAnalyze=true -AnalClassId=1  -AnalTestPort=100  -IgnoreColumns=symbol,datetime,rm30,ram20,sl6,sl12,ram30,sl60,sl20,sl90,sl3,sam10,sl30,rbm20,rbm10,sam20,sam180,sam360,sbm90,sbm180,sbm360


cd %XXCWD%
