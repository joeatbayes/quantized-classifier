# Deep Learning for Stock Price Prediction Explained

Originally Published on [linkedin](https://www.linkedin.com/pulse/deep-learning-stock-price-prediction-explained-joe-ellsworth) February 17, 2017

As part of my work on [Quantized Classifier](http://%28https//bitbucket.org/joexdobs/ml-classifier-gesture-recognition) I have built a set of examples showing how to use Deep Learning to predict future stock prices. Tensorflow is a popular Deep Learning library provided by Google. This article explains my approach,  some key terminology and the results from the set of examples.  The code is free so please [download and experiment](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition).

![img](https://media.licdn.com/mpr/mpr/AAEAAQAAAAAAAAxXAAAAJGMyNjJhNDQwLWM3ODctNGQ4OC05MGE2LTAyMTJlODdiYTIyMw.jpg)

Related Articles: [Stock Price Prediction Tutorial](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/wiki/stock-example/predict-future-stock-price-using-machine-learning.md), [Analyzing Predictive Value of Features](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/demo/stock/spy/1-up-1-dn/docs/stock-price-prediction-analyze-feature-value.md), [FAQ](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/docs/faq.md), [How to make money with Quantized Classifier](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/wiki/how-can-i-use-quantized-classifier-to-make-money.md)

### General Purpose Tensorflow CNN Classifier

The first step was building a general purpose utility that could read a wide variety of CSV input files submit them to Tensorflow's CNN for classification. The utility needed to work across a wide range of inputs from classifying heart disease to predicting stock prices without any changes to the code. This utility is called [CNNClassify.py](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/tlearn/CNNClassify.py) When used for stock price prediction it reads two CSV files a training file and a Test file. It outputs the classification results to the console. It builds a deep learning CNN using the training data and then uses the CNN to classify rows from the test data file. It then generates output showing how successful it was in the classification process.

You need to install Tensorflow, TLearn and python 3.52 to run these samples.

### Classes Explained

In supervised learning we look at a given row of and assign a class. You can think of a class as a grouping of rows. Any classification project requires at least two classes such happy or sad, Alive or Dead. For these examples I use class=0 to indicate a given BAR that failed to meet the goal. Class=1 if the BAR did meet the goal.

We are seeking bars that will rise in price enough to meet a profit taker goal before they would encounter a stop loss or that rise at least 1/2 of the way to the goal before reaching a maximum hold time.

To determine the class we look ahead at future bars and determined if the price for that symbol has moved in a way that would meet our goal. For these stock examples we have three factors for each goal.

1. A Percentage rise in price that would allow exit with a profit taker order.
2. A point where if the price drops by more than a given percentage will exit the trade with stop limit.
3. A maximum hold time where if the price has not risen to at least 1/2 of the way to goal before the hold time expires it is considered a failure.

Bars that meet satisfy these rules are assigned a class of 1 while bars that fail are assigned class 0. These classes are used by the learning algorithm to train the machine learning model. They are also used to test verify the classification accuracy of the model when processing the test file. In a production trading system the predicted class is used to generate buy signals that could be executed either by a human or an automated trading system.

In our examples we seek to maximize precision and recall of class 1 to find successful bars. The premise is that we will eventually use predicted classes for current bars to generate buy signals.

- **Win / Loss Magnitude is important:** It is important to note that some samples target a profit taker much larger than a the than stop loss. This means that winning transactions will yield a larger gain on average than what is lost when loosing trades exit at the stop limit. This approach helps reduce the total # of trades which can reduce trading costs while still maximizing profits. It also means than you still generate a profit even if you win less than 50% of the time. If you get a precision of 50% for 2X average profit versus average loss then it will be quite profitable. You will need this context when comparing results.

In a more sophisticated system we could have dozens or hundreds of classes but in this instance we are only seeking a signal about whether it is a good time to buy a specific symbol using a specific goal set. It would be relatively easy to run the engine across hundreds of stocks so you always had something available to buy.

The Utility we use to generate the training and test data files with the classes assigned is [**stock-prep-sma.py**](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/8aab8c92d0478037c9dcd5145d62e240aa7c9ebd/stock-prep-sma.py?at=default&fileviewer=file-view-default) You need to have used the utility to download the Bar data before running it. You can use your own bar data or [yahoo-stock-download.py](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/yahoo-stock-download.py) will download it from yahoo. It is only a sample but it can be a good example of where to start building a more sophisticated system.

The class computation used in these tests is simplified. Feel free to take these samples and add your own creative enhancements. The combination of different classification logic and different feature engineering can allow a single engine like Quantized classifier to produce millions of different trading signals all customized to each specific users trading preferences.

### Base Probability and Lift

When evaluating any machine learning system there are several numbers we use to measure how effective the system is.

- **Base Probability** - Given a input test data sets a certain portion of bars will be class 0 and a certain number will be class 1. If 33 bars out of 100 met the goal then the base probability that any bar will be of class 1 is 33 / 100 = 0.33
- **Precision** - When the system runs across test data it attempt to classify bars. How often the actual class of a given bar matches the given bar is called precision. If the system predicted that 27 bars would be class 1 and only 22 bars actually were class 1 then the precision for class 1 is 22 / 27 = 0.8148 The precision can also be measured for all records in a system but in our context we care the most about the precision of class 1 because we plan to use it to generate buy signals.
- **Recall** - When the system evaluates test data it will attempt to find all the bars that it should classify as a given class. In reality it will only find a fraction of the bars that are available. Recall is computed as a ratio of those it classified correctly and the total number of records of that class. A general rule is that you can increase recall at the expense of precision or increase precision at the expense of recall. Better engines and improved feature engineering are used to increase both. Recall is typically computed on a class by class basis. We care most about recall for class 1 because higher recall will generate more buy signals. If there were 33 bars available and the system correctly found 22 bars that it classified as class 1 then recall for class one would be 22 / 33 = 0.66.
- **Lift** - Lift is the measure of how much better precision is than base probability. Lift is important because it allows comparison of the relative improvement in prediction accuracy that remains comparable even when base probability changes. If Base probability is 0.33 and precision is 0.8148 then lift = 0.8148 - 0.33 = 0.4848. I use lift to help guide exploration of features if I can increase lift without a dramatic reduction in recall then it is normally a good change.

### Understand Probabilities in context:

A common mistake is to look at a precision such as 55% out of context of the Goal. I could be right to look at 55% and say it is poor odds. But if you tell any gambler you will give them 55% odds and on winning hands they will earn 3 times as much as they loose with loosing hands they will gamble all week long.

The law of large numbers indicates that if they have a 55% chance of winning and they are betting $100 each time after a large number bets they they will have won 55 times and lost 45 times average per 100 bets. They would have won 55 * $200 = $11,000 from the wining bets. They would have lost 45 * 100 = $4,500 in the loosing bets. giving them a net profit of $6,500 As long as the magnitude of the win versus loss stays the same and the probability of win versus loss stays the same then they will continue making profit. The law of big numbers also indicates they could have a long run of losses in the short run and still average 55% in the long term so they need to manage the amount they bet using something like the [kelly criteria](http://bayesanalytic.com/tag/kelly-criteria-algorithm/) but overall it is a winning system.

I intentionally choose samples where the amount won is larger than the amount lost because I found that when we force a larger win magnitude it helps isolate the signal from the noise which helps the prediction system deliver greater lift. This normally comes at the cost of recall so we have fewer trades but I would rather run dozens of diverse strategies that earn more profit per trade with greater chances of winning.

### Feature Engineering

Feature engineering is where some of the most important work is done in machine learning. Many data sets such as bar data yield relatively low predictive value in their native form. It is only after this data has been transformed that it produces useful classification.

In the context of our stock trading samples we used a few basic indicators which are applied across variable time horizons to produce machine learning features.

1. Slope of the price change compared to a bar in the Past
2. Percentage above minimum price within some # of bars in the past
3. Percentage below the maximum price within some # of bars in the past
4. Slope of Percentage above minimum price some # of bars in the past
5. Slope of percentage below maximum price some # of bars in the past.
6. Each of these may be applied to any column such as High, Low, Open, Close or they can be applied against a derived indicators such as a SMA.

The utility that produces files with the machine learning features and classes is called [stock-prep-sma.py](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/8aab8c92d0478037c9dcd5145d62e240aa7c9ebd/stock-prep-sma.py?at=default&fileviewer=file-view-default) It is only intended as an example that you can modify to add your own creativity. I do not claim these are great features but they were good enough to demonstrate Quantized classifier and Deep Learning CNN delivering some lift and reasonable recall.

Feature engineering is an area with nearly infinite potential for creative thought which means that machine learning classifiers like Quantized classifier can produce radically different trading signals for different users. I encourage you to explore this area there are hundreds of indicators explained across thousands of trading books most of which can be converted into machine learning friendly features.

### Deep Learning number of epoch explained

The Tensorflow flow Deep learning CNN (Convolutional Neural Network) a learning strategy based on how scientists think brains learn. The C portion essentially adds multiple layers to the NN which can allow them to perform better in ares where decision trees have previously dominated.

Just as biological systems learn best with repetition the CNN needs to see data multiple times while it is building its internal memory model it uses to support the classification process. Each repetition where the training data is re-submitted to the CNN engine is considered one epoch.

I have generally found minimum acceptable results are at 80 repetitions while the CNN seems to perform best with at least 800 repetitions when working with this set of indicators for stock data. Each of these repetitions is what the Tensor-flow libraries call a epoch or evolution. 

For this these samples I chose to use 800 epoch. For those that did not produce good results I increased number of epoch to 2800.

### Have fun and Experiment

> Before you ask if I have tried it with X data set? Or if it has been hooked to broker X. The Engine is free, the examples are free. You are free to take them and test them with any data or configurations you desire. Have fun and please let me know what you learn. If you want help then I sell [consulting services](http://bayesanalytic.com/contact).

**Sample Call**

```
CNNClassifyStockSPY1Up1DnMh3.bat

OR

python CNNClassify.py ../data/spy-1up1-1dn-mh3-close.train.csv  ../data/spy-1up1-1dn-mh3-close.test.csv 800

```

**Sample Output**

![img](https://media.licdn.com/mpr/mpr/AAEAAQAAAAAAAArCAAAAJGExMjRmMmNiLTUxMzItNGM2OS05NzFjLTY1ODQyODBlMjg3OA.jpg)

### 

### CNN Related stock tests

Parm 0 = CNNClassify.py the script python will run, Parm 1 = Training File to use when building internal memory model. Parm 1 - Test file to use when testing the classification engine. Parm 3 - Number of Epoch to use for this test.

[CNNClassifyStock-SLV-1p5up0p3dnMh5.bat](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/tlearn/CNNClassifyStock-SLV-1p5up0p3dnMh5.bat) - SLV (Silver) Goal to rise by 1.5% before it drops by 0.3% with max hold of 5 days.

```
python CNNClassify.py ../data/slv-1p5up-0p3dn-mh10-close.train.csv  ../data/slv-1p5up-0p3dn-mh10-close.test.csv 800

```

 [CNNClassifyStock-SPY-2p2Up1p1DnMh6.bat](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/tlearn/CNNClassifyStock-SPY-2p2Up1p1DnMh6.bat) - SPY Goal to rise to exit with profit taker at 2.2% with a 1% stop limit. Max hold of 6 days.

```
python CNNClassify.py ../data/slv-1p5up-0p3dn-mh10-close.train.csv  ../data/slv-1p5up-0p3dn-mh10-close.test.csv 800

```

[CNNClassifyStock-SPY-6p0Up1p0DnMh45.bat](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/tlearn/CNNClassifyStock-SPY-6p0Up1p0DnMh45.bat) SPY goal to rise to exit with profit taker at 6% gain with stop loss at 1% and max hold time of 45 days.

```
python CNNClassify.py ../data/spy-6up-1dn-mh10-smahigh90.train.csv  ../data/spy-6up-1dn-mh10-smahigh90.test.csv 800

```

 [CNNClassifyStock-SPY-8Up4DnMh90.bat](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/tlearn/CNNClassifyStock-SPY-8Up4DnMh90.bat) SPY Goal to rise to exit with profit taker at 8% gain with stop loss at 5% and maximum hold time of 90 days.

```
python CNNClassify.py ../data/spy-8up1-4dn-mh90-close.train.csv  ../data/spy-8up1-4dn-mh90-close.test.csv 800   

```

[CNNClassifyStock-SPY-1p0Up0p5DnMh4.bat](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/tlearn/CNNClassifyStock-SPY-1p0Up0p5DnMh4.bat) SPY Goal to rise to exit with profit taker at 1% gain before it encounters a stop loss of 0.5%. Max hold time 4 days.

[CNNClassifyStock-CAT-1p7up1p2dnMh2.bat](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/tlearn/CNNClassifyStock-CAT-1p7up1p2dnMh2.bat) CAT Goal to rise to exit with profit taker at 1.7% before it encounters a stop loss at 1.2% with max hold of 2 days.

[CNNClassifyStock-CAT-6p0up1p0dnMh45.bat](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/tlearn/CNNClassifyStock-SPY-6p0Up1p0DnMh45.bat) CAT Goal to rise to exist with profit taker at 6% before it encounters a stop loss at 1% with max hold of 45 days.

[CNNClassifyStock-CAT-7p8up1p2dnMh5.bat](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/tlearn/CNNClassifyStock-CAT-7p8up1p2dnMh5.bat) CAT Goal to rise 7.8% to exit with profit taker before it encounters a stop loss at 1.2%. Max hold of 5 days.

### Deep Learning Tensorflow disclaimer

Deep learning is a broad topic area. Tensorflow is a fairly large and complex product. I have used one configuration of a Tensorflow CNN for these examples. Tensorflow supports many other models and CNN can be configured in many ways including a different initialization and different layer configurations. There are most likely ways to configure Tensorflow to produce better results than I have shown in these samples.

### Summary

This work is only intended to provide a starting point from which you can easily branch out with your own discovery process. I do sell [consulting services](http://bayesanalytic.com/contact) you can purchase if you would like to use my expertise to accelerate your own work.

I wrote these examples to test the [Quantized classifier](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition) and for some of the samples it delivers substantially better results than Tensorflow did. This may be due to selection biased where I was seeking examples that performed well with the Quantized classifier. 

It may be possible to find a configuration of Tensorflow the would deliver superior results.   For me is seems easier and faster to find profitable combinations using the [Quantized Classifier](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/wiki/stock-example/predict-future-stock-price-using-machine-learning.md) and [Quantized filter](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/quant_filt.py)    The Quantized library also seems to provide better support to help [discover which features are adding predictive value](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/demo/stock/spy/1-up-1-dn/docs/stock-price-prediction-analyze-feature-value.md?at=Adding+By+Feature+and+By+Feature+Group+Analysis&fileviewer=file-view-default). Having the engine help guide the feature selection can be an immense help when there are millions of possible feature and indicator combinations but only a small number of them will actually help predict future stock prices.    This could be purely a manifestation of the fact that I know the internals of the quantized classifier better. 

### Request for comments

If you would like to build the [Quantized classifier](http://bitbucket.org/joexdobs/ml-classifier-gesture-recognition) into a larger trading system then we can help by [providing expertise and consulting services](http://bayesanalytic.com/contact).

Please let me know if you would enjoy similar articles exploring the same examples using the Spark ML libraries or other popular ML libraries.

I am still a little disapointed that Tensorflow found no tradable oportunities for some of the strategies when the Quantized filter did find some.   If you find alternative configurations with Tensorflow that produce better results then please share them with me so I can update the article.



Thanks [Joe Ellsworth contact](http://bayesanalytic.com/contact)  [linkedin](https://www.linkedin.com/in/joe-ellsworth-68222) CTO and principal research scientist

[![Joe Ellsworth](https://media.licdn.com/mpr/mpr/shrink_200_200/p/1/000/02f/0b0/3543e7e.jpg)](https://www.linkedin.com/in/joe-ellsworth-68222)