# Trading related support for Quantized Classifier



## Overview



## Key Files



## How to Use







# TODO / ACTIONS:

- Add the Google CSV Bar downloader to replace the yahoo downloader and update the documentation to show it.
- Add Analyzer which reads the training data set and shows the stats for each column for each numBuck from minNumBuck to maxNumBuck.   Want to see the precision + recall for each number of buckets or at least see which maxNumBucket provides the  best precision per column.  Need to optionally score by  by  precision or (precision * 3) + recall precision cost so we have some influence from the recall.    Need The precision is computed by first building the quant table then predicting the value for each record in the training data set then comparing the predicted class against the computed class.   The precision for each class is computed by #number of correct predictions / # of predictions for that class.      The actual precision for a feature is computed as sum(precision_for_each_quant_bucket) / Number of quant buckets.
  - New Article computing the value of differing input columns for Machine Learning
  - Presumably we should be able to isolate the number of quants that deliver the greatest value and which number of quants are optimal for that feature.  
- What feature did I build that reports on basic information or precision gain. I remember looking at it but it is not currently showing in the main readme.  We need this for the finance work.
- Produce a feature that shows what number of quants for each feature produces greatest information gain.     Generate a function which analyzes the input data set and shows a function of information gain for each feature for each number of buckets from 1 to MaxBuck.  This can be used as input in future feature selections.   EG:   The features which provide the greatest information gain from the minimum number of quants will generally provide best predictive value with least risk of over learning.        
  - One possible way to compute information gain is to compute the number number of items correctly classified / total number of items.   This gives a ratio similar to inverse entropy where a higher number represents a higher quality classification result.
    - The actual measure of entropy would be  number incorrectly classified / total number of items.   
    - A variant of this is used to allow the inputs to includes a set of 1 or more classes where we only measure the information gain for the classes we care about.  That way we can better ignore the center distribution we do not care about but in this instance we run a significant risk of over precision so we would want to modify the number to be precision / 
    - ​
    - In this context is for 2 to MaxNumBuck compute information gain 
- Implement walk forward predictor /  Incremental training indicator   Trains on first X% of bars then predicts on the next bar then adds that bar to training set and predicts on the following bar. 
- Integrate Backtest with the incremental training indicator
- Implement mechanism to train choose best symbol out of a set of bars.
- Implement the true tree based selector that can select which columns should be treated as a probability versus tree based selector.   I think the tree based selector should be applied first then apply probability columns within the context of the bucket inside the tree.  https://sebastianraschka.com/faq/docs/decision-tree-binary.html   https://towardsdatascience.com/decision-trees-in-machine-learning-641b9c4e8052  https://machinelearningmastery.com/classification-and-regression-trees-for-machine-learning/   https://homes.cs.washington.edu/~shapiro/EE596/notes/InfoGain.pdf  https://en.wikipedia.org/wiki/Information_gain_in_decision_trees https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/  http://people.revoledu.com/kardi/tutorial/DecisionTree/how-to-measure-impurity.htm https://en.wikipedia.org/wiki/Information_gain_ratio https://www.analyticsvidhya.com/blog/2016/04/complete-tutorial-tree-based-modeling-scratch-in-python/  http://pages.cs.wisc.edu/~jerryzhu/cs540/handouts/dt.pdf  https://en.wikipedia.org/wiki/Decision_tree_learning https://medium.com/machine-learning-101/chapter-3-decision-trees-theory-e7398adac567  https://www.xoriant.com/blog/product-engineering/decision-trees-machine-learning-algorithm.html http://www.cs.princeton.edu/courses/archive/spr07/cos424/papers/mitchell-dectrees.pdf
  - As applied to quantized classifier we could use the notion of the cost analyzer from the decision trees to find which number of buckets for each feature provides the most pure split.    EG:   We have the minimum number of mixing in each output class.
  - We can use the classes which provide the most pure  splits with the smallest number of quants as the early inputs or pure filters for things latter grouped by the probability functions. 
- ​

