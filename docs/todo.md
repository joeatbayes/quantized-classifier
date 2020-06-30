#Future Work List#
**Please comment and critique.**  I need your help to ensure future work is prioritized to help the people actually  using the library.  http://BayesAnalytic.com/contact



### Current thoughts Feb-2018

* One weakness of Quantized classifier is that for data with a majority set dominating for any single class  tends to overwhelm the statistical probability for similar records that have a different outcome.  This is one reason it does not do as good for some defect classification as desired.  EG:  If any single class is extremely dominant for some features eg: 99.999% of all widgets are OK while only 0.001% fail then just about every feature measured will tend towards to predict success because normally that measurement would yield success.  When there are a set of measures eg: color is yellow instead of white that where the yellow is more dominant does that feature really help.   

  If 99.999% of the yellows are also success then the probability based system will predict that yellows will be successful.  To solve this we need a different where the probabilities of the dominant class do not damp out available signal. 

  Lets use the yellow / white ratio again if we know that all the failure units are yellow or even that say 70% of all failure units are yellow this could be critical information especially if we know some other attributes such as weight could be used in a similar fashion then the two when combined can yield important information.      

  Another example is that in a strongly trending market there are still days or periods of time when the price moves counter trend.    These counter trend moves represent interesting profit opportunities if they can be reliability predicted.  Most of the probability models struggle to differentiate these counter trend days because most computed indicators in that time frame resulted in pro-trend movement.   

  If we are producing 10 million units per day then even at 99.999% success we know that we are likely to produce 100 failures.  Our job is then to find the characteristics of the 100 failure units.   The math has to change so rather than measuring  the raw probability of a given sample belonging to minority class we can possibly measure the the portion of the minority class that occur for that measurement.    Using our color example again.     If  yellow & Red colored units contain 90% of the failure units we can treat them a 0.9  even though they still have a base probability 99.999% of being sucessful but white units only contain 10% of the failure units I want to say t

  * Need to practice early per feature analysis to better determine which features support finding or classifying the minority class nodes.
  * logistics regression or SVM may be a better approach for this condition. 

* Extend the analyzers to include ability to try the Quantized algorithm,  Logistics Regression,  SVM,  Decision tree and recommend which classifier to use for each data set.  Make it easy to report of information gain by feature then make it feasible to store this configuration for future runs on the same data set so it remembers which classifier to use for each feature.  May be worth trying a LVQ ( Learning vector quantization) as one of the classifiers.

##Focus Areas##

There are several focus areas where I can invest time. Please let me know if you have an opinion for prioritizing between them. 

* **Implement the optimizer / discovery aspect.**  I explain some of this in the [Genomic research white paper](genomic-notes.md) The optimizer allows the engine to take a large set of features and determine which features are more import for accurate prediction.  Which features hurt prediction.  How different features should be grouped into different sized quanta buckets.       In a Healthcare scenario the optimizer not only improves the prediction quality but it could help researchers to discover that Age is less important than they thought while Bits 1,13,27 in chromosome Y are very important for predicting Condition X when bit 1 and 13 are turned on but bit 27 is turned off.
* **Implement Data Correlation discovery feature**.  The easiest way to think about this is when analyzing stocks if we find particular clusters of data where more than one stock moves in same or opposite direction then it can imply a correlation that may be useful when predicting future price movements.  EG:  if we found that the slope of current prices % above minimum 30 day price has a cluster at 0.2% where both CAT and SPY are found to have clustered values then it reflects a correlated facet. 
* **Implement the Quantized Filter Algorithm in GO** This version more closely approximates the multi-layer approach used in CNN in TensorFlow but with a drastically different approach.  It can provide better output when there is a benefit from eliminating matching on a class when there is a negative match for a given feature such that there is no matching quanta from the test set.  This could allow us to do even a better job of important discovery and can provide better capacity on eliminate featurs that negatively contribute to prediction accuracy. 
* **Finish the HTTP wrappers to allow it to run as REST service.**   This could be helpful to allow the classification engine to be integrated with a VR engine running on a different piece of hardware or written in a different language. This could be important when analyzing data sets with lots of classes because the data sizes could become larger than could be contained in mobile devices. 
* **Implement Time Sequence recognition** Some gestures must start with a given pose that transitions between a series of poses ending in a termal pose. Recognizing these moving gesture recognition may be acomplished by classifying several input sets across time then running as a set through a second classifier.  Since all humans will not move at the same rate one interesting aspect will be allowing for variable time between the poses. 
* **Implement the text parsing version**.   Many common demonstration systems use text databases like IMDB and attempt to classify input text against those movies.  This is interesting but has a lot of overlap with search engines.  See [Text classification overview](docs/text-classification/overview-classification.md)
* **Implement the image parsing version** so we can test against ImageNet and Minst.   Much of the TensorFlow work is demonstrated parsing and classifying images. I didn't not invent the quantized classifier for engines but it would be interesting to see how it performs. 
* **Optimize for Image Classification**   I am not sure this is worth while because image classification is one area where CNN and other Deep learning seem to perform very well with relatively little tuning. 


## PR Work

- stocks: Write article on using specified category columns
- stocks: Copy Stock price prediction trade to Bayes Analytic Blog
- stocks: Copy Stock Price prediction article to Linked in Blog
- stocks: Copy feature analysis article to Bayes Analytic Blog
- stocks: Convert SLV30 to demo article 
- stocks Convert SPY90 to demo article
- stocks: Write Article showing how to use category column and ignore column with detail output to make it easier to read the classifier output since it can show both the Stock and the bar date time in the output columns. 
- Article: Write article showing how to use the Category and Ignore Features it should also define them.   Can use example from credit example to illustrate category files.
- Write feature permutation article / demo

##Roughly prioritized Feature Work##

* Analyzer: Add capability to modify decay function using a passed in function pointer. Current decay rate of 0.8 is OK for general purpose but there could be other conditions where alternatives such as log of delta from max would work better.  Another alternative is using a Portion of the difference from best score to worst score. 

* ​

* Stock: Add a Round trip example stock trading system that keeps the bars updated for a set of symbols. Makes continuous predictions and makes the data available via a web service. 

* > * stocks: Modify the Stock prep file to allow the parameters to be supplied by external parameters rather than applying them from code changes. 
  > * stocks: Enhance the Yahoo stock downloader to download data for most recent bars to only update bars that do not already exist in the BAR file.  Stocks: Need to modify stock downloader to download many symols from list and update most recent BAR.   Should to this by porting the python code to GO to keep the python dependency as small as possible to allow online version.   Should include feature to pull current day from system clock rather than hard coded.  Should be able to run multiple times per day and save result in BAR file as last bar. 
  > * Stocks: Implement the stock viewer Showing the chart with entry / exit points.  Would be easier if generator includes the entry, exit point.  to support this would need the number of bars held. 

* stocks: Implement a Initial Correlation analyzer.   Download 20 different BAR files where each symbol is converted into a class.  Once we identify with analyze features optimal bucket sizes then choose a number of buckets near max buckets or possibly near 20 buckets.   Find the set of buckets that have the largest total counts for the system as these should represent the most strongly correlated symbols and give us a rough data value for the correlation.    The Sort by NumBuck, BuckCnt, ClassCnt seems to identify heavily trafficked buckets that should represent strong correlation if fed with data for multiple symbols. 

* > * Stocks: Double check the new symbol and bar date are copied to detailed output file.  Fix if it that is not true. 
  > * stock: To support correlation version we either need to be able to process multiple symbols through the stock_prep logic converting each symbol into a class or we need  create multiple files with the indicators included and then transform those into a single file containing different classes.  Since we still have success and failure conditions we would need a strategy to map the symbols uniquely across these classes eg:  SPY 0=fail, 1=sucess,  CAT 2=fail,3=success, AA 4=fail,5=success.
  > * Stocks: Need a feature to merge multiple stock BAR files into single file while retaining symbol.  Will also need a feature to convert symbol name to class name.   Need this to support the correlation analyzers.
  > * stocks: Write a script that downloads the N symbols runs the analyzer across them and reports on the set that yields the best performance based on current system of indicators. 

* Enhance classifier to read saved model code to  rebuild in memory model rather than retraining.  NumOfBuck is the number of bucket used to generate this line whiel buck# is the actual computed buck ID.  We need both because our model includes records for all values from 1 to maxBuck.

* Write the Analysis Feature Permutation Add simple analysis component that shows predictive value of different groups of features compared to other groupings of features.   Add analysis component that randomly combines feature combinations in twin and tripplets to see if we can find sets that provide good predictive value superior using features individually.   This should probably be done using the quant filter combination so each mini set is working as a mini decision tree.

* Feature Analyzer:  The user should be able to control the rate of decay in feature weight.   And the rate of decay should be a function of how much less precise the column is than the best column or should  be relative to the difference between the  best and worst column.   EG:  If to features are at 72% and 71.9% then their difference should be relatively small but if one is at 72% and another is at 55% and the one at  55% is the lowest then it should have it's precision reduced accordingly.  Add Analyzer classifier a command option so the set divisor can be either number of features or adjusted weight based on feature weight.

* Enable category for class where string classes are mapped into integer values but need to regenerate the original class when saving the results. 

* Add Ability to include mini-feature sets groups of fields in the quant prob model to be applied as Quant Filter instead of Quant Prob.   This could either be done by the primary quant prob engine or possibly by an external component that essentially create the feature groups and takes the statistical output from them to build a new file which is fed into the quant prob engine.  This approach would help isolate complexity but may be slower.   For example  if we find that day of week + hour of day + % above Min represents a good feature group using the quant_filter aspect then comming out of that engine we know the relative probability by class.   May be able to combine this into a single feature using a range for each class but it may be easier to create a new column one for each class  that contains the probability the quant_filter found for that feature group for that class.  Then we could suppress the actual features in the input set.  In the short term the easiest way to run this would be to generate an intermediate file but if it works well should be done as virtually added columns. 

* Enhance Model Save to also save meta data needed to allow loadModel to function where that data can not easily be placed in the  model detail file. 

* Implement LoadModel to restore model state from files created by saveModel.  Also add print model that produces human friendly version. 

* Implement browser display utility to display in nice format data from saveModel

* Split the work for training and classification out to multiple cores.   May as well read X lines in chunks and allow each one to process the input.   Will be easy for classification but may require synchronizing the models for training to avoid two threads updating the same buckets simultaneously but could still have one core doing the load and split,  another core doing the convert to float and a 3rd core doing the document update.   Could also possibly have each core build their own model and merge the counts at the end which would scale better for a distributed architecture.     Another approach would be to switch the trainer so it is feature centric so they share a input set of rows but each process / core is only updating one feature which would remove the risk of overlapping count updates.  Also write a document on how this is approached for the Bayes blog. 

* Write  a blog on bayes for approaching text classification.  Based on [Text classification overview](docs/text-classification/overview-classification.md) 

* Add ability in CSV Files for command line parser to specify a column other than column #1 as the class.  

> - Only include detail probs if requested.   
> - Choose column to use as class

* Normalize Output Probs so the sum of all classes  in any prediction for a given class is 1.0  But need to make sure this doesn't mess up confidence  of prediction between multiple lines.  May need to   take an approach of dividing by the number of columns  that could have contributed rather than those that  actually contributed then when we scale up it would 
  provide more accurate output.  The We are currently  apply the count for only the features that have a matching  bucket to be more accuate we need to apply feature weight to the divisor even if we didn't get a match for the feature  for that class.


* Update rest of filenames links in readme.md to link to local source for the same file. 


* Add Shell script alternatives for each of BAT file. 
* Produce GO version of the Quant Filter to see if we can improve performance on the diabetes and titanic data set.  The Quant filter is unlikely to deliver 100% recall since it aborts the match as it traverses the features when it fails to find a matching bucket id. This gives it some precision filtering capability similar to the multi-layer convoluted NN but at a lower cost.  We may be able to add probability since it is still computed by class by feaure. There some chance that more than one class will survive all layers of the filter which would mean we need to add a probability to that output to act as a tie-breaker. 
  - Add optimizer to quant filter that allows it to  vary the number of buckets by feature.  Seting number of buckets to 1 essentially turns a feature off by forcing all items into the same bucket. The primary cost function is total number of buckets. The goal of optimizer is based on starting with all buckets equal to X.  As it varies the number of buckets
    by feature it can keep the change provided it can  increase precision as long as recall does not decrease. Or it can increase recall as long as precision does not decrease recall.  We can discourage over learning by always trying a smaller number of buckets first in the optimizer.  A natural side effect of this is that the engine can turn off
    features that do not contribute either accuracy or recall.
    get. 
  - The weakness of the current QuantFilt strategy is that it tries to find the most restrictive quant able to make a match but when it fails it moves to the next least restrictive set of quanta for the entire matching process.  What we really want is for it to back track only for the feature where the most restrictive match did not work reduce the restriction only for that feature and keep the more restrictive requirement for the others.   This is complex because overly restrictive setting at any feature can cause failure in all subsequent features the the back track has to work it's way back incrementally.  


*   Modify Quant_prob run as server handler. 

    *   Method will use main as data set name unless &dset is specified.
    *   Each named data set is unique and will not conflict with others.
    *   Method to add to training data set with POST BODY
    *   Method to add to training data set with URI to fetch.
        * Allow the system to skip every N records to reserve for 
        * testing.
    *   Method to classify values in file at URI 
        * Allow &testEvery=X to only test every Nth
          item.  This is to support testing.     
    *   Method to classify with POST multiple lines.
    *   Method to classify with GET for single set of features.
    *   Allow number of buckets to be set by column name
    *   allow column name to be set map direct to bucket id

*   Implement the samples with [AWS MXNet](https://aws.amazon.com/blogs/compute/seamlessly-scale-predictions-with-aws-lambda-and-mxnet/) libraries for comparison. 

*   Implement the samples with Spark ML for comparison

*   Produce a version for text parsing that computes position  indexed position of all words where each unique word gets  a column number.   Then when building quantized tree               lookup of the indexed position for that word  treat the word  index as the bucketId or possibly as columnNumber need to think  that one through buck as a bucket id seems to make most sense and then treat all the other features as empty. So the list of cols may grow to several million but will only contain the hashed classes for those value. Allow system to pass in a list   of columns n the CSV to index as text.  This would not effectively use word ordering but we could use quantized buckets for probability of any word being that text in text string so  a word like "the" that may occur 50 times would occur in a different bucket when it is repeated many times. 

     ​

# Completed Items Phase 1 #

* DONE:JOE:2018-02-10: Stocks: Add Indicator the % above % below Min, Max and slope of percentage above low / min max.
* DONE:JOE:2017-02-09: Implemented with explicity -classOut parameter. Modify Analysis save file name to be explicit parameter instead of implied from test out file name.   Our change the semantics for the system to supply a working base name that we derive everything else from so that it is explicity used for that purposed. 
* DONE:JOE:2017-02-09: Stocks: Modify Stock prep scripts to include the Symbol and BarDateTime as columns of output in the CSV.  Need to add these to all stock scripts as ignore columns.   Also includes updating all scripts to reflect new output names.   Also need to update documentation that links to the update scripts.
* DONE:JOE:2017-02-09: Stock need to modify exit condition to include a maxHold period.  Where success is price > than target at max Hold. 
* DONE:JOE:2017-02-09: Fix Problem of script loading analysis output is not returning identical results to the analyze output and  it should.  Turned out be be dealing with a copy of rec in ieterator so had to set the weight directly.
* DONE:JOE:2017-02-08: When generating model file using category columns It should output the original string value instead of current high low value. 
* DONE:JOE:2017-02-08: Modify trainer to read the analysis file when available and respect the min/max number of buckets by feature and skip generating counts for those out of bounds.  This should save memory and allow larger models to be ran on smaller computers even though you still need a larger computer to perform the analysis step. 
* DONE:JOE:2017-02-08 Add classifier option to supress some columns by name.  
* DONE:JOE:2017-02-08 Update CSV Parser to automatically build a class ID for CSV columns that contain string values.   The first time it sees each value assign it a integer value from the series.    Will need to save those values to allow reverse mapping.   Also need to support this for the class columns.


* DONE:JOE:2017-02-08:Enable ignoreColumn where that column is simply copied through the system into the detail output file in it's original form but not used for the classification process. This can make it easier to keep BarDate and Symbol in the Bar files when used for correlation. 

* DONE:JOE:2017-02-08: Switch from type int16 to TClassId and int32 to TQuantId to improve understandability and provide better hints of purpose to reader.

* DONE:JOE:2017-02-08: Enable CategoryColumn for features where unique strings are mapped to unique integers rather than typical bucket logic.    When generating detail classification then the original category label should be copied out into the detail output file.  This should support less work than forcing all values to be converted to int or float.   If we have both then feature name and bar date could be represented natively with less plumbing work.   MaxBucket, MinBuck should not be applied for Category values. 

* DONE:JOE:2017-02-08:Add Category Sample script.  Note: Found credit example with lot of category values

* DONE:JOE:2017-02-08: Feature analyzer Make the apply weights optional for feature analysis

* DONE:JOE:2017-02-08: feature analyzer Finish the sort selector to apply weights to use the correct precision indicator based on setting for selected class or no class depending on whether the request used a selected class.

* OBSOLETE:2017-02-07: Write a script that can read normal CSV and convert string input columns into integer values based on the number of unique values it finds.  It needs to determine which columns are safe to consider numeric and which ones must be converted.   Whoudl be able to specify category columns at command line.  Should be able to suppress columns at command line. 

* DONE:JOE:2017-02-07: Enhance analysis component to set feature weight by percieved value / accuracy of that feature.

* DONE:JOE:2017-02-07:Create ClassifyAnal module to create output Statistics

  - DONE:JOE:2017-02-07:Output should include Add recall, precision by class in classifyFiles
  - DONE:JOE:2017-02-07:Convert output of run from byte array to a structure that can be retained and used as output by optimizer to compare quality of output against other runs. 
  - DONE:JOE:2017-02-07:Add report of base prob by class so we can see how the Accuracy of the class compares to the base probability or measure Lift.

* DONE:JOE:2017-02-07: Enhance classifier to save model as CSV file.   eg: feat#, NumOfBuck, buck#, class#, TotCnt,  classBuckProb,  buckFeatPob, classProb where classBuckProb is the probability of that class within the bucket and buckFeatProb is probability of that bucket relative to all values, Class prob = probaiblty of that class within set.   Implement Model Save that  Saves the model wide parameters in INI file key=value Saves the model wide parameters in INI file key=value / parameters in file fiName.model.txt  Saves the feature defenitions in CSV format. featureNum, NumBuck, FeatWeight, TotCnt, Bucket1Id, Bucket1Cnt, Buck1EffMinVal, Buc1MaxVal, Bucket1AbsMinVAl, Bucket1AbsMaxVal Where each of the Bucket1  features are repeated for 1..N buckets.  This should give us everything we need to restore a model with  all of it's optimized settings intack.  It also gives us a nice representation to support the discovery aspects of the system.  function saveModel

* DONE:JOE:2017-02-01: Add by class reporting to tensorflow script results.

* DONE:JOE:2017-02-04: Add a simple analysis component that shows the predictive value of each single feature.  eg: run the classifier for a single feature varying numBuck for that feature.

* DONE:JOE:2017-02-04: Add a analysis component that analyzes predictive value of each feature column.    It should be able to measure the value for total precision of the set or for a combined input on predictive value by class.   It should seek to find a number of buckets for that feature that will maximize predictive value from that feature and be storable so the set of these values can be used to configure operation of the primary classifier.    

* DONE:JOE-2017-02-05: Enhance analysis component to save and restore analysis outputs with optional command parameter so the analysis can be used to influence future runs of classififier.

* DONE:JOE:2017-01-30: Enhance QuantProb classifier so when classifying a given column we use the largest number of buckets possible then fall back for that column to a lesser number when we get a miss on the number of buckets.  This means we need to create the index for 2 to N buckets which means we need to add one more layer to the model builder.   This should allow us to use the most specific value match we can with reasonable fallback. 

* DONE:JOE:2017-01-30: Fix the Breast Cancer demo that is currently reporting 75% accuracy.  The Bucket # seems to be messed up.  In a column with a value range from 1..10 and numBuck=10 it is assigning value 2 to bucket 92. 

* DONE:JOE:2017-01-29: Enhance quant_filt.py to support two file inputs one for train and one for class.  Also include set and by class analysis of results.

* DONE:2017-01-29: Enhance quant_filt.py to support choosing the most precise answer in maxNumBuck it can for each row falling back to less precise numBuck as needed to find a answer.

* DONE:JOE:2017-01-24: Support -class versus -test option as input to classifyFiles

* > - DONE:JOE:2017-01-24: Implement -class option for 3rd input file in classifyFiles
  > - DONE:JOE:2017-01-24: Classify Files needs to support both the test mode and a classify mode.
  > - DONE:JOE:2017-01-24: Should generate the correct output .test.out or .class.out
  >
  >
  > - DONE:JOE:2017-01-24: Added command line parser library to support more complex command line needed to support optimizer. 
  >

* DONE:JOE:2017-01-24: Add descriptions to file names in readme.md where they do not already exist or remove those files.

* DONE:JOE:2017-01-24: Add links to bat files for new test data structures. 

* DONE:JOE:2017-01-24: Add the call to setGoEnv to all BAT that build the GO libraries.

* SKIP:JOE:2017-01-24: Modify the CSV parser to use the [faster binary Bulk IO method that I tested with the GO](https://github.com/joeatbayes/StockCSVAndSMAPerformanceComparison) performance test.     

* DONE:JOE:2017-01-24: Test the relative performance of reading the CSV line by line using their built in method while appending parsed rows rows to a slice versus scanning the file to count the number of lines then pre-allocating the slice at the correct size and grabbing the rows out of a memory byte level memory buffer.  JOE: Read by line using new buffered IO class is just as fastDONE:2017-01-20: Implement the TLearn / Tensorflow equivelant of
  >     classify files.  It could be named CNNClassifyFiles
  >     since the first implementation would use a convoluted
  >     neural network.

* DONE:2018-01-18: Add Command Parser to TLearn/CNNClassify.py so it can be driven externally by command line parameters.

  ​

* DONE:2017-01-20 Test the classifier against Image data to see how it performs.  State of the art seems to be a 16% error rate. Will need a way to incrementally update the engine image by image rather than reading all the data from a CSV.  Try it first just by converting the images native.   Then reduce the images to greyscale and try again just to see how it does.  Will need to buy a larger hard disk.   http://image-net.org/download-imageurls  http://image-net.org/  https://en.m.wikipedia.org/wiki/ImageNet  At the very least this set of images would be great to test a image search engine.    I suspect we will need to analyze the image in smaller blocks and then classify them individually.    The best strategy would likely be to attempt to trace similar colored objects after applying an averaging filter then classify based on the vectors. http://farm1.static.flickr.com/32/50803710_8cd339faaf.jpg  As shown here differentiating the background from primary object and accomodating different scale of primary object along with different postion will be the most challenging.  

>>> I tested it with data for mnist and I cifar-10 with mnist best quantizer score for cifar was  31% compared to 36% for the Tensorflow CNN.   With mnist digit classification the best score for quantizer  was 51% while the CNN scored over 91%.    It is a little surprising the Qauntizer did as well as it did on the cifar data since it has no support for subjects moving within the frame of the data.   It could be improved but image classificaiton doesn't seem like a good place to invest with the excelent work already being done in that area.    A surprising aspect is that when n_epoch was low between 5 and 8 the CNN speed improved to be nearly comparable to the speed of the Quantized classifier.   I did find the n_epoch needed to be about 150 to get good precision out of CNN on these data sets and then it was 5 to 10 times slower. 

- DONE:2018-01-18: Update QuantProb to properly scale buckets to   cope with outliers to prevent them from negatively affecting   spread for normal distribution items.

