XXCWD=$(pwd)
cd ../../../../

classifyFiles -train=data/spy-1p0up-0p5dn-mh4-close.train.csv -test=data/spy-1p0up-0p5dn-mh4-close.test.csv  -testOut=tmpout/spy-1p0up-0p5dn-mh4-close.out.csv -model=tmpout/spy-1p0up-0p5dn-mh4-close.model.csv -maxBuck=500 -testOut= tmpout/spy-1up1-1dn-mh9-close.out.csv -IgnoreColumns=symbol,datetime -LoadSavedAnal=false

cd $XXCWD
