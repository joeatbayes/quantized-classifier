::
::   Seek profit taker exit at 1.5% before
::   encountering stop limit at 0.3%
::   max hold 5 days. 
::
set XXCWD=%cd%
cd ..\..\..\..\

classifyFiles -train=data/slv-1p5up-0p3dn-mh10-close.train.csv -test=data/slv-1p5up-0p3dn-mh10-close.test.csv -testOut=tmpout/slv-1p5up-0p3dn-mh10-close.out.csv -minBuck=50 -maxBuck=110  -detToStdOut=false -doPreAnalyze=true -AnalSplitType=2 -AnalClassId=1  -AnalTestPort=100 -IgnoreColumns=symbol,datetime,sam90,sam360,sbm360,sl6,sbm20,rbm20,sl3,rbm10,sl60,sam20,sl12,,sl90,ram30



cd %XXCWD%