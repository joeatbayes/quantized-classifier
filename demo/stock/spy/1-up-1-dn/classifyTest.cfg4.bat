::rm classifyFiles.exe
::go build src/classifyFiles.go
::
:: Attempts to classify data based on which bars will
:: go up to exit with profit taker at 2.2% before 
:: they drop to a stop limit at 1%.  Those that go up are 
:: classified as 1 those that drop are classified as 0
:: The classification step is done by stock-prep-sma.py 
:: which also splits the data between train and test file.
::
:: To Run the Stock example on SPY data first run the 
:: the utility to download data from yahoo python yahoo-stock-download.py
:: then run utility to convert raw stock data into machine learning
::  data python stock-prep-sma.py then  you can run
:: this module.

set XXCWD=%cd%
cd ..\..\..\..\

classifyFiles -train=data/spy-1p0up-0p5dn-mh4-close.train.csv -test=data/spy-1p0up-0p5dn-mh4-close.test.csv  -testOut=tmpout/spy-1p0up-0p5dn-mh4-close.out.csv  -LoadSavedAnal=false -maxBuck=20 -IgnoreColumns=symbol,datetime,sam10,ram30,sam20,sl3,sbm10,sbm20,sl6,sl60,sl30,sl20,sam90,sam180,sam360,sbm90,sbm180,sbm360

cd %XXCWD%

