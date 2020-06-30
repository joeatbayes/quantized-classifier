:: To Run the Stock example on CAT data first run the 
:: the utility to download data from yahoo python yahoo-stock-download.py
:: then run utility to convert raw stock data into machine learning
::  data python stock-prep-sma.py then  you can run
:: this module.

:: Goal Rise by 7.8% to profit takers before Before 
:: Stop limit at 1.2% would be hit.
:: Max hold is 5 days.

:: Demonstrates using only a subset of the columns initialized
:: by analyzer as high value. 
::
set XXCWD=%cd%
cd ..\..\..\..\

classifyFiles -train=data/cat-7p8up1p2dn-mh5-close.train.csv -test=data/cat-7p8up1p2dn-mh5-close.test.csv -testOut=tmpout/cat-7p8up1p2dn-mh5-close.out.csv  -model=tmpout/cat-7p8up1p2dn-mh5-close.model.csv  -minBuck=290 -maxBuck=300 -detToStdOut=false -writeFullcsv=true -doPreAnalyze=true -AnalClassId=1  -AnalTestPort=100  -IgnoreColumns=symbol,datetime,sam20,sl90,sl6,sl60,ram30,ram20,sl12,sbm10,rbm10,sam10,sam90,sam180,sam360,sbm90,sbm180,sbm360


cd %XXCWD%
