# DEFER Items

- Finish filling in sections of the [Genomic research white paper](genomic-notes.md). Add Test set for Daily stock bar data.  Where we add a column which is a SMA(x) where X defaults to 30 days. and features are the slope of the SMA(X) when comparing current bar to SMA(x) at some number of days in past create.  In a stock scenario  you would have a goal EG: A Bar for a symbol where price rose by P% within N days without dropping by more than Q% before it reached P%.  Those that meet the rule get a class of 1 while those that fail get a class of 0.   

- ​

- Defer further work on the optimizer until I have reconciled where the responsibility of the Analyzer stops or how the two features are supposed to interact:   Add QProb optimizer that is allowed to change Feature weight and number of buckets.

- > - List optimizer settings at end of run
  > - Implment optimizer save and restore feature
  > - implement optclear feature including delete existing opt settings file.
  > - Implement -OptCycleClass
  > - implement -optClear
  > - implement -optSave
  > - implement -optMinRecall
  > - ​
  > - DONE:JOE:2017-01-28 Add OptClassOption
  > - Implement a option to allow the quantized classifier to store the entire array of training data in memory pre-converted to arrays of floats.  This will allow much faster re-train when changing the number number of buckets in the optimizer.    Also Requires Modify the classifier core to accept row with array of flow.  Separate the parsing / conversion form the training. 
  >
  > > - Add Retrain from RAM option which causes CSV util to pre-parse float array.  Will need one fast scan to count lines.  Need to borrow the fast version of that I wrote to support the comparative testing.
  > > - Add ability for training and classify to be ran from an array of pre-parsed float.   Need this to support speed during optimizer runs.   Ideally if input file size is below a threshold we would retain in RAM otherwise we have to scan form disk to avoid consuming all available ram. 

- > - DONE:JOE:2017-01-24: Improve optimizer specification on ClassifyFiles 

- > - Implement a -describe option to better explain reasoning output
  > - Implement option to describe high priority features  in optimizer.
  > - Implement option to describe high priority patterns for high priority features. EG: Those sets of values from the quants that deliver the greatest  predictive input for each identified class.
  > - Allow only a single feature to be retrained.  This is needed to support speed when allowing the optimizer change number of buckets for a feature. 
  > - weight and feature number of buckets seeking to maximize precision at 100% recall. Where total number of buckets is considered primary cost.  Minimum number of buckets is equal to 2.  a Feature can be turned off by setting it's feature weight to 0. 
  > - Optimizer needs ability to reserve some data from training data set to use for training.  It needs to periodically change which data is reserved.  EG: It may choose every 5th record for a while then switch to every 10th record.   It Also needs choice to use only last x% of set for optimizer setting when running with time series data.
  > - Optimizer rules.   Can keep change if precision increases while recall stays the same.  Can keep the change is recall rises while precision remains the same. Can keep change is both precision and recall rise.   Can keep change if precision rises but recall doesn't drop below a configured threashold.    When changing number of buckets must always try  1 bucket,  1/2 current number of buckets,  random number between 1 and max buckets.   When changing  priority of a feature it must first try a priority of 0,  then a priority of 1/2 current priority, then random number between 0  and maxPriority.   When changing features the system must ensure all features are checked so first try 3 random features then 1 feature from each end working from the end towards the other end.    
  > - ​