See [genomic-notes.md](genomic-notes.md)

#Minimizing Overlearning in Optimizer#

> TODO: Fill this in 

#Choosing Number of Quanta Buckets.  More is not always better#

> TODO: Fill this in


#Outliers Detection & Handling#
One possible problem with a quantized engine is that if the 
data set is noisy and contains data for any feature that is 
abnormally high or low this can create a large range which can
cause the quanta buckets to be created larger than desirable.

An example of this is that stock values move day to day a 
relatively small amount normally under 1%. Every so often
a price could move by a larger amount such as 12%.   When 
used for prediction we are more interested in the movements 
of 97% of all bars so we want the numeric range used to compute 
the quanta size to reflect the min, max values of those 97%
of bars closer to the center of the distribution of values.
If the average daily movement is 1% and we are using a 10 
quanta system the bucket size would be 0.1%.  If we do not
suppress the influence of outliers we would use a 12% range
so each quanta would be sized at 1.2% which would make all 
the normal data values clump together into a single quanta 
bucket which would remove the usefulness as predictive values. 

To remove undue influence from the outliers we want must 
detect the values of the top and bottom extreme values which 
normally requires sorting all the training values.  Since our
training data set will likely exceed available ram the load 
and sort does not work.  

What we do is take the absolute
minimum and absolute maximum values to divide each value read
for a each feature evently between 1,000 buckets.  We keep 
a separate set of counts called a distribution matrix for 
each feature.  

We can scan from the Bottom of the distribution matrix
accumulating counts until we have enough records to represent 1.5% 
of the data and then scan from the max value down. 

Once we find the distribution buckets with the outlier values
eliminatedit becomes a matter of simple math
to compute new effective minimum and effective maximum values.
We use the new effictie min/max values to compute new quana 
bucket sizes.  The actual buckets are based on a sparse matrix 
so the extreme values get large bucket Id
but that is actually desired.

The system defaults to setting the effective range by removing the
influence from 1.5% of the total row set from each end.  This can be 
change if needed.  The actual code is implemented in 
[src/qprob/classify.go](src/qprob/classify.go) in the function 
setFeatEffMinMax but it is enabled by the 1000 bucket distribution
grid that is built in [/src/qprob/csvInfo.go](/src/qprob/csvInfo.go)
in the method BuildDistMatrix().


#Temporal Reinforcement#

  One of the features provided by convoluted neural networks is the 
  ability to have some more recent records influence classification 
  results more than other records.   

  This can be supported for 
  Quantized probability system by allowing the system train against
  the entire set and then re-train with more recent data multiple times.

  The system computes a probability value for each feature based on how
  many times the bucket value occurred for a given class divided by the 
  total number of records.  By applying more recent data many times 
  it increases both the class counts favoured by the most recent data 
  plus the total record count.  This will give those newer records a higher 
  probability input.   

*    An extension to this could be to look at the span of
     of time covered in the training set up front and automatically adjust
     the count using a multiplier as we move through the training data
     from old to new.  This would be a relatively easy
     enhancement to add. 

     ​
