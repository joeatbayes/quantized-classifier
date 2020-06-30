:: This classify Test requires data that must be 
:: downloaded from a separate site and then converted
:: into our CSV format.  
:: See: convert-cifar-10-to-csv.py for download 
:: and conversion instructions. 
::
:: NOTE: The training input is over 500 megs so it 
::  takes this one a few minutes to run. 
::
classifyFiles -train=data/cifar-10.train.csv -test=data/cifar-10.test.csv -numBuck=255 -testOut=tmpout/cifar-10.test.out.csv
