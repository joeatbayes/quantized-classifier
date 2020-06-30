# Home Data Value Assessment



## AVM - Automated Value Model

AVM (Automated Valuation Model) to predict a market value of unsold properties.  

 I am  not hoping for a perfect fit, but a new way of looking at an old problem.  I am thinking there are similarities between  your work and what we will be working on next.    I need to get you a better overview so you can determine if this will be feasible or not.  I don't want to replicate the same old thing.  I have done that once already, it was good, but it wasn't amazing



## Joe's Thoughts

* For Chris
  * Property clustering or classification is intricately linked to property value model prediction.  I don't think they can be treated as two separate problems.  Explained below. 

- The most simple version of this is to use a set of quants per attribute such as # bathroom, Age,  SQ Foot then simply say those that match on the largest number of quants  are the strongest affinity cluster and should have similar values.
  - Would likely need a weighting system to allow different features to be provided greater weight in the matching system.
  - Would want a regression optimizer so for each attribute we choose a number of quants that delivers the most accurate predictions of home value 
  - May need a geohash or other value that can be used to identify location preference.   EG:  A small home in Park city will carry a much higher premium than the same house in South Jordan.  With that said it may be feasible to create a premium value grouping where price values are similar even if geographically disbursed.   EG:  East bench of SLC  should be  similar to East bench of Provo where the gross values of the homes may be substantially different but the clustering of a feature such as size would be similar.
- Basic statistical approach will struggle due to housing price clusters in specific neighborhoods.  It seems that we need to use neighborhood price clustering first then we may be able to use other properties like age,  property size,  # baths to compute a relative on a scale between the high and low property values in the area.   Can we derive location preference from a synthesis 
- Need to find a way to cluster properties  so we can find the most similar properties in the local areas.
  - Once we do this then we can compute most similar property values based on cluster.
  - Once cluster is Identified we would want to computer where the value sits in the cluster.  EG:  If the cluster identified has a price range between 100K and 120K then we need to compute where in that range the price falls.   We might be able to do this by identifying a numerical range for something like square footage, acreage, etc where the properties price relative 
  - This seems to be a fairly typical clustering problem most often tackled with a K-Means clustering algorithm https://en.wikipedia.org/wiki/K-means_clustering     K-means quite often  struggles with the large number of attributes so we must simplify or find an alternative approach.
- Quantized Cluster:
  - Take a value such as SQ Foot finished.   Break it into  10 discrete values eg:   800 to 1000,  1001 to 1300,  1301 to 1500.    For each of these quants identify % value above minimum in the area as an average.   This average will likely need to be based on local area rather across entire state because some cities like Park City have a definite preference impact on price.   Question will the value of the predicted price in a given quant remain consistent across the region or do we need to model  the quants specific to the regional preference.
  - A nested quantized cluster can be used to deliver more precise value adjustments.   EG:    We could use the SQ foot finished size as  a primary feature with a sub feature of # of bathrooms or Home age in years.  This would yield a feature grouping so homes between 800 to 1000 sq foot and between 1 and 5 years are considered one quant.   This is a powerful way to building affinity but it can also rapidly over constrain sets meaning each quant is so small that we get less value from the law of large numbers.  Net net is we want at least a few hundred rows in each discrete quant but can sometimes get away with a few dozen depending on the domain. 
  - ​
  - ​







### Background: 

Talking to the DataMaster Attorney, he would prefer DataMaster not be directly involved with this project, but license the intellectual property to a third party entity, retaining marketing rights to the private sector.  By contracting through me (or a third party entity specific to this), that can be achieved and MCAT will receive a perpetual user license for the public sector.  MCAT again pays for the expenses associated with the modifications.  DataMaster can then market the product through their existing private sector channels.  Optional associated royalties can be involved.

Looking at what you have been doing with stock predictions highly correlates with these two projects.  The derivative work can be combined with DataMaster’s intellectual property to produce something unique.  I also have a statistician working on the problem and we think we have a concept to move forward with.  He has done some analysis with IBM’s SPSS and the results look promising.  



# county-sales CSV File Data Notes:

- Tx_dist is tax district
- Valarea is value area
- PT is property type
- SPT is a subset of PT (specific property type)
- N_Grp is a property cluster or grouping (neighborhood group)
- LEA is Land Economic Area (another grouping)
- PL_Value is Primary Land Value (this value is associated with up to the first acre of land, there is an associated tax exemption)
- PCTCOMPLETD is the percent complete of the building (most are one for 100%, associated with new construction)
- YRBLT is the year built
- EFFAGE is effective age in years(data is subjective)
- Remodyr is remodel year (associated with next column for percentage of improvement that was remodeled)
- BLTASSF is above ground square footage
- BSMT is Basement (BSMT_Total is size of basement and BSMT_FIN is the finished area in basement)
- The Bath columns indicate how many fixtures in that bath.  Bath2 is a half bath with toilet and sink.
- ATTGAR is attached garage size
- DETGAR is detached garage size


- Column BN is a sale validity code.  Y is a valid sale, anything else is not (B = bank owned, S is a short sale)