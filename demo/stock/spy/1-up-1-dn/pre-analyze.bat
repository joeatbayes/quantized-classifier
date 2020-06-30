set XXCWD=%cd%
cd ..\..\..\..\

classifyFiles -train=data/spy-1p0up-0p5dn-mh4-close.train.csv -test=data/spy-1p0up-0p5dn-mh4-close.test.csv  -testOut=tmpout/spy-1p0up-0p5dn-mh4-close.out.csv -model=tmpout/spy-1p0up-0p5dn-mh4-close.model.csv  -maxBuck=50 -detToStdOut=false -doPreAnalyze=true AnalClassId=1 -AnalTestPort=100 -AnalAdjFeatWeight=true -IgnoreColumns=symbol,datetime,sbm180

cd %XXCWD%