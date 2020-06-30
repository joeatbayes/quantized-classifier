:: To Run the Stock example on CAT data first run the 
:: the utility to download data from yahoo python yahoo-stock-download.py
:: then run utility to convert raw stock data into machine learning
::  data python stock-prep-sma.py then  you can run
:: this module.

:: Goal Rise 1.7% Before Stop limit at 1.2% would be hit.
:: Max hold is 2 days.  This makes average gain 141% of
:: avg loss.  This means we need a win rate of 30% to 
:: break even.    
::
:: Demonstrates using only a subset of the columns initialized
:: by analyzer as high value. 
::
set XXCWD=%cd%
cd ..\..\..\..\

classifyFiles -train=data/cat-1p7up1p2dn-mh2-close.train.csv -test=data/cat-1p7up1p2dn-mh2-close.test.csv -testOut=tmpout/cat-1p7up1p2dn-mh2-close.out.csv  -XXmodel=tmpout/cat-1p7up1p2dn-mh2-close.model.csv -minBuck=20 -maxBuck=75 -detToStdOut=false -writeFullcsv=true -doPreAnalyze=true -AnalClassId=1  -AnalTestPort=100  -IgnoreColumns=symbol,datetime,sam20,ram20,sbm10,ram30,sbm20,sl90,sl30,sam90,sam180,sam360,sbm180,
:: sbm20,sbm10,sl20,rbm20,sl3,sl60
:: sl6,,sbm10,,sam20,,,,,,sl30,sl90,sl12,sam10,ram30,sbm20,sl60,rbm20,ram20,sl3,sl20,rbm10
::

cd %XXCWD%
