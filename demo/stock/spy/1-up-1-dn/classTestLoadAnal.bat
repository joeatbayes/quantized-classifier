set XXCWD=%cd%
cd ..\..\..\..\

classifyFiles -train=data/spy-1p0up-0p5dn-mh4-close.train.csv -test=data/spy-1p0up-0p5dn-mh4-close.test.csv  -testOut=tmpout/spy-1p0up-0p5dn-mh4-close.out.csv -maxBuck=50 -detToStdOut=false -LoadSavedAnal=true -IgnoreColumns=symbol,datetime

cd %XXCWD%