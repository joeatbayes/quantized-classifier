:: Example of using the pre-analyze feature
:: to discover important features and important
:: data clusters within the important features.

classifyFiles -train=data/diabetes.train.csv -test=data/diabetes.test.csv -minBuck=30 -maxBuck=40 -testOut=tmpout/diabetes.test.csv  -detToStdOut=false -doPreAnalyze=true  AnalTestPort=100 -AnalAdjFeatWeight=true  -model=tmpout/diabetes.model.det.csv
