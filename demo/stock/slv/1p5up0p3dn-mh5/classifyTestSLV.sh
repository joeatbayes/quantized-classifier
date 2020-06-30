#::
#::  Seek profit taker exit at 1.5% before
#::  encountering stop limit at 0.3%
#::  max hold 5 days. 
#::

XXCWD=$(pwd)
cd ../../../../

classifyFiles -train=data/slv-1p5up-0p3dn-mh10-close.train.csv -test=data/slv-1p5up-0p3dn-mh10-close.test.csv -testOut=tmpout/slv-1p5up-0p3dn-mh10-close.out.csv -maxBuck=400  -LoadSavedAnal=true  -IgnoreColumns=symbol,datetime,sbm10,sam20,sam10,sl6,sl30,ram30,sbm20,ram20,sl3,sl90,sl60

cd $XXCWD
