::rm classifyFiles.exe
::go build src/classifyFiles.go
::
::
:: To Run the Stock example on SPY data first run the 
:: the utility to download data from yahoo python yahoo-stock-download.py
:: then run utility to convert raw stock data into machine learning
::  data python stock-prep-sma.py then  you can run
:: this module.

:: Seek profit taker exit at 6% rise
:: before hitting stop loss at 1% 
:: max hold 10 days

set XXCWD=%cd%
cd ..\..\..\..

classifyFiles -train=data/spy-6up-1dn-mh10-smahigh90.train.csv -test=data/spy-6up-1dn-mh10-smahigh90.test.csv -testOut=tmpout/spy-6up-1dn-mh10-smahigh90.out.csv -minBuck=550 -maxBuck=570  -IgnoreColumns=symbol,datetime,rbm10,rbm20,sl3,sbm10,sam10,sbm20,ram30,rbm10,sl3,sl12,sl90,sl60,sam10,sl6,sl20,,sam90,sam180,sam360,sbm90,sbm180,sbm360

cd %XXCWD%