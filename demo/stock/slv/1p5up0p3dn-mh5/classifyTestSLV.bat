::rm classifyFiles.exe
::go build src/classifyFiles.go
::
:: To Run the Stock example first run the 
:: the utility to download data from yahoo python yahoo-stock-download.py
:: then run utility to convert raw stock data into machine learning
::  data python stock-prep-sma.py then  you can run
:: this module.
::
::  Seek profit taker exit at 1.5% before
::  encountering stop limit at 0.3%
::  max hold 5 days. 
::
set XXCWD=%cd%
cd ..\..\..\..\

classifyFiles -train=data/slv-1p5up-0p3dn-mh10-close.train.csv -test=data/slv-1p5up-0p3dn-mh10-close.test.csv -testOut=tmpout/slv-1p5up-0p3dn-mh10-close.out.csv -minBuck=50 -maxBuck=110  -LoadSavedAnal=false  -IgnoreColumns=symbol,datetime,sam90,sam360,sbm360,sl6,sbm20,rbm20,sl3,rbm10,sl60,sam20,sl12,,sl90,ram30

cd %XXCWD%
