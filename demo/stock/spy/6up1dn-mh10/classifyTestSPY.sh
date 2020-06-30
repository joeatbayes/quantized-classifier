:: Seek profit taker exit at 6% rise
:: before hitting stop loss at 1% 
:: max hold 10 days

XXCWD=$(pwd)
cd ../../../../

classifyFiles -train=data/spy-6up-1dn-mh10-smahigh90.train.csv -test=data/spy-6up-1dn-mh10-smahigh90.test.csv -testOut=tmpout/spy-6up-1dn-mh10-smahigh90.out.csv -maxBuck=100  -IgnoreColumns=symbol,datetime,rbm10,rbm20,sl3,sl6,sbm10,sam10,sbm20,ram30,rbm10,sl6,sl3,sl12,sl90,sl60,sam10,sam180,sam360,sbm90,sbm180,sbm360

cd $XXCWD