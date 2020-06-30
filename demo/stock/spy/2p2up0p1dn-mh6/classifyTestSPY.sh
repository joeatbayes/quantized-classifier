#:: Seek profit taker exit at 2.2% rise
#:: before hitting stop loss at 1% 
#:: max hold 6 days


XXCWD=$(pwd)
cd ../../../../

classifyFiles -train=data/spy-2p2up1-1dn-mh6-close.train.csv -test=data/spy-2p2up1-1dn-mh6-close.test.csv -testOut=tmpout/spy-2p2up1-1dn-mh6-close.out.csv  -minbuck=500 -maxBuck=510  -IgnoreColumns=symbol,datetime,rbm10,rbm20,sl3,sl6,sbm10,sam10,sbm20,ram30,sam180,sam360,sbm90,sbm360


cd $XXCWD