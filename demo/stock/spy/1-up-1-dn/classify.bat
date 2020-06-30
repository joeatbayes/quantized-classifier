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
classifyFiles -train=data/spy-1p0up-0p5dn-mh4-close.train.csv -class=data/spy-1p0up-0p5dn-mh4-close.class.csv  -testOut=tmpout/spy-1p0up-0p5dn-mh4-close.out.csv -model=tmpout/spy-1p0up-0p5dn-mh4-close.model.csv -maxBuck=500 -LoadSavedAnal=true  -IgnoreColumns=symbol,datetime,sam90,sam180,sam360,sbm90,sbm180,sbm360 -writeFullcsv=true -writeCSV=true 
cd %XXCWD%

