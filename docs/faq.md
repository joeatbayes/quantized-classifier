# Facts Questions & Answers Quantized Classifier

[TOC]

#### Did you hook Quantized classifier stock predictions up to your brokers api and run a live test?

> I answered this in the [FAQ](https://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/docs/faq.md ) and in [How to make money](https://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/wiki/how-can-i-use-quantized-classifier-to-make-money.md).   Here is a more specific answer.    I have provided the classification engine and samples of how to use it for predicting stock prices.  
>
> The classifier and samples are freely available for you to take and use with your broker.  Feel free to test the engine with your own broker and with your own ideas for indicators.  All you risk is your time and whatever you choose to invest. 
>
> I am willing to [provide consulting services](http://BayesAnalytic.com/contact) to help you integrate [Quantized Classifier](https://bitbucket.org/joexdobs/ml-classifier-gesture-recognition)  into your trading system. 
>
> When I personally use Quantized Classifier for trading I will use it to predict on a longer time horizon so the trades can be made manually while using the Quantized classifier to help identify entry and exit points.    
>
> > *When I am using Quantized Classifier to support Live trading,  I will not publish or share the indicators or configuration I am using for live trading because it would throw away my competitive trading advantage.*    *I may not even admit I am using it for live trading.*
>
> It will require additional investment of integrating additional indicators as predictive features before the system would be ready to use for live trading.   I provide [examples of how to produce indicators](../stock-prep-sma.py) and [examples of how to feed the data](../demo/stock/spy/1-up-1-dn/?at=default)  into the Quantized Classifier engine to provide classification services.    I explain the process of adapting samples into a full fledged system in [Stock Price Prediction ML Tutorial](https://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/wiki/stock-example/predict-future-stock-price-using-machine-learning.md).   
>
> > I do not feel it is worth the cost & hassle of maintaining all the production grade linkages to support full auto trading unless you are trading enough capital to justify the IT Integration and support costs.   I have built and operated all these kinds of integrations in the past for both the Stock and Forex but you need to be ready to make an investment in both trading capital and OpEx to really make automated trading pay off.   There are silly obstacles that require money to overcome:
> >
> > * The IB (Interactive brokers) API fails whenever there is a blip in internet connectivity and refused to login again until a human does so with a hokey password lookup card.   Just hope a internet blip doesn't occur when you are on a plane with a lot of money at risk.  Net, net the IB API is unsafe unless you can afford to pay people to be available to re-connect the system after connection failures. 
> > * The TDA API is more reliable but imposes a high minimum cost per trade with a minimum of 25K at risk in the automated trading account.  The high TDA trade costs require either large capital at risk or large percentile movements.  
> > * The IB API imposes stupid fees like a charge every time you change the stop or profit taker limits which the big players do not pay.  This makes it cost prohibitive to use intelligently moving limit orders that I found are essential to overcome some of the gaming behavior of the high speed traders.    
> >
> > You can bypass a lot of the obstacles when trading sufficient money by using a higher quality broker with low trading fees plus a FIX API but that requires a minimum of about 250K at most brokers and you must recertify the API at every broker you trade through.   They will typically not certify an API until you have the money on deposit with them.   Even when you meet their minimum balance requirements you many brokers also require a minimum # of transactions per month to retain access to their API. 
> >
> > One reason I do not invest in either IB or  TDA API directly for use with the Quantized Classifier repository is that their data use agreements prohibit publishing any derived results including graphs,  trading results,  published signals, etc.    It just doesn't make sense to invest in using a data source that I don't plan to actively trade and which prohibits secondary publishing of derived works.  
> >
> > If you have the budget and appetite to deploy a fully automated trading system then the Quantized classifier is a great kernel to build the system around.   I am qualified and  willing to [sell the consulting services](https://BayesAnalytic.com/contact) to build the rest but please understand that while the rewards can be huge there is also substantial risk and a substantial up front investment to get started.



#### Have you tried Quantized classifier that on [Numer.ai](https://www.linkedin.com/redir/redirect?url=Numer%2Eai&urlhash=SJR0&_t=tracking_anet)?

> I publish the repository so others can use it as they desire  including use with Numer.ai.  
>
> Stock prediction is something the engine can do but I am focused on the general purpose machine learning engine. The ability to provide [stock predictions](https://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/wiki/how-can-i-use-quantized-classifier-to-make-money.md) is a side effect.    
>
> A stock price prediction does require a good ML prediction engine  but even a  great engine can be crippled without good data.    The fact that Quantized Classifier was able to produce  good results using simplistic indicators (features) shows great promise but I do not claim the current set of indicators published as examples are good enough to use for live trading.  
>
> A  majority of [trading related work](https://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/src/default/demo/stock/spy/1-up-1-dn/docs/stock-price-prediction-analyze-feature-value.md) is centered around feature engineering, trading rules and infrastructure plumbing style coding.    This is interesting work but it is not the same as producing a general purpose machine learning prediction engine.   Functionality built into Quantized classifier can greatly reduce the cost of evaluating  features for their predictive value which may be as valuable as the predictive capability. 
>
> Every day invested in feature engineering is a day less invested in a core engine features.   For the immediate future I will be focused on improving the core prediction engine features because that is where my skills are most valuable.
>
> My willingness to invest in supporting the proprietary Numer.ai API and additional stock feature engineering depends on who is willing to [buy consulting services](http://BayesAnalytic.com/contact) .    I am happy to help clients who want to apply the Quantized classifier engine to stock price prediction and need specific features or need help in feature engineering. 



#### How Can I make money using Quantized Classifier

> I answer this question in some detail in a [related article](https://bitbucket.org/joexdobs/ml-classifier-gesture-recognition/wiki/how-can-i-use-quantized-classifier-to-make-money.md)   The quick answer is take the engine and use it as a component in a larger trading system.    This can be as simple as having it send you email when it is a good time to buy SPY or as complex as using it to automatically trade hundreds of symbols.    The Core engine is very adaptable but you still need to do the work to integrate it for use with your own feature engineering and apply your own trading rules.      
>
> Building high quality prediction engines is a expensive and highly specialized skillset.   Engineers who are good at it are very rare and most publically available engines produce marginal results.    We are giving you a free engine along with working price prediction samples that could cost millions of dollars to build from scratch if you are lucky enough to find a engineer capable of delivering it.   Feature engineering still requires skills but can be accomplished by a larger group of less expensive data scientists and even casual coders.   Plumbing and trading rules are well understood problems that can be implemented by readily available and less expensive engineers. 
>
> A fundamental rule in trading is that more traders copying profitable trading systems will dampen out the same irregularities that created the profit opportunity.  As such the late arriving copycats nearly always loose money.    This implies that you need to add some sort of unqiue and differentiating value which implies you do not want to use the easy off the shelf system that makes the same decisions as thousands of other traders.   Quantized Classifier is a component well suited to acting as the nucleolus of your unique trading system.     I am willing to [sell consulting services](http://BayesAnalytic.com/contact) to help you build the rest. 
>
> There is a general rule in IT that low cost engineers quite often ruin even well designed core engines by building poorly concieved layers of infrastructure around them.   It can produce superior results to use superior but more expensive engineers to build complete systems.   This can seem more expensive since highly talented people can cost 5 to 10 times what readily available commodity engineers cost.  The unfortunate reality is that I have seen many projects where companies have invested millions of dollars abandoned after years of effort by dozens of people because they did not have the right team of superior engineer / architects in place.    It is increasingly common to see companies required to rebuild products from scratch because they can no long maintain the accumulated cruft accumulated from average engineers.    I have made most of my income for many years selling services to companies where I fix  or at least remediate these kinds of systems.  It is always many times more expensive to fix the systems than it would have been to build them correctly in the first place.   The net lesson is that hiring cheap engineers tends to waste more money than it saves.     I [sell consulting services](https://BayesAnalytic.com/contact) to help clients build successful systems. 

