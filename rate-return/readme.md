# Rate of Return Demo #

By Joseph Ellsworth July to .... 2017    206-601-2985  see:  http://BayesAnalyic.com

## Abstract

Attempts to apply machine learning across a wide range of stocks to predict those stocks most likely to rise over the next defined time period.   In the most simplistic approach we train a series of stock across time assuming that we purchase X5 of those that generate the strongest Buy signal and sell those with the strongest sell signals.    

Symbols are purchased on a given day and sold a specified number of days latter unless they violate a optional stop loss.  A more advanced version adds a trailing stop that activates after the symbol has gains a specified percentage of profit. 

A secondary system attempts to balance risk by limiting total long exposure and total short exposure for each sector based on the sector balancing rules.   

The machine learning algorithm applied  is the  Quantized Classifier produced by Bayes Analytic.   Extended tests using tensorflow CNN may be applied.

One interesting variable  that will be tested is whether total system yields are better when training and prediction are made against each symbol when trained against all symbols in the same sector or when classified against history for that specific symbol.





## Summary Results



## Approach

* Convert EOD data into standard Bar Files
* Add the computed indicators rate of return by month, rate of return by day as a new set of files.
* ​

### Critical Variables

pBuy =  The % of those to buy based on strongest signal.

pSell = The % of those symbols to sell based on strongest signal.

holdDays = The number of days to hold a given symbol after purchase.

  

## Files








## Resources ##
* Adapted some concepts from:  Applying Deep Learning to Enhance Momentum Trading Strategies in Stocks by  - December 12, 2013 Lawrence Takeuchi * ltakeuch@stanford.edu Yu-Ying (Albert) Lee yy.albert.lee@gmail.com




