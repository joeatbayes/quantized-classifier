#:: Seek profit taker exit at 8% rise
#:: before hitting stop loss at 4% 
#:: max hold 90 days


XXCWD=$(pwd)
cd ../../../../

classifyFiles -train=data/spy-8up-4dn-mh90-close.train.csv -test=data/spy-8up-4dn-mh90-close.test.csv -testOut=tmpout/spy-8up-4dn-mh90-close.out.csv   -maxBuck=40 -IgnoreColumns=symbol,datetime,ram20,sl3,sl12,rbm10,sl30,sl20,sam180,sam360

cd $XXCWD