#Genome Prediction of Outcomes #
> **Predicting things like the Risk for Breast Cancer**
>
> This section explains how the Quantized probability machine learning classifier could be used in the context of genomic research.   It can provide classification services where it learns from sample data how to analyze pieces of a genome to help diagnose specific conditions.   It also explains how the classifier can help identify pieces of the genome most valuable for a given prediction.
>
> > I am not a [Genome](http://www.healio.com/hematology-oncology/learn-genomics/genomics-primer/chromosomes/chromosomes) expert but I have interacted with people who work on Genomic tools and have picked a up a little knowledge along the way.  **Please correct my vocabulary and explanation to be accurate.**
>
> This approach is based on the premise that if a genome is stretched out it can be modeled as a series of of 0 and 1 stretched out in a very long array.  Researchers isolating regions of this data they think can help predict susceptibility to various conditions.    They analyze for patterns to predict a given outcome such as Has Breast Cancer = 1,  Does not have Breast Cancer = 0.   Other patterns can identify Sex, propensity for brown hair, etc. 
>
> In machine learning we take whatever slice of the genome the researcher thinks might may contain important data along with the a class for that row such as 1 if they are Male, 0 if they are female.    Once the system is trained  it can be fed data for new genome input and  attempt to predict the class of the new sample.    
>
> ### What is a Feature ###
> > In the context of a genome each unique 0 or 1 in the sequence is considered a facet.   If you think of it as a CSV file the the first column would be used as a predictor then there would be 1..N columns each representing a bit of data.   A slice of Genomic  data can be thought of as Comma delimited list like:
> >
> > * 0,0,1,0,1,1,1,1,1,0,0,1,1,0,1
> >
> > More complex models may assign a number between 0 and X for each position in the genome. 
> >
> > The slice could be pulled from a single portion of the genome or could be pulled from several different sections and assembled as one longer slice.   The first number is generally the measured outcome or class while others are measures from the data.  Data from other sources such as Age or previously ran tools can also be included as features.  This could yield an input like: 
> >
> > * 0,40,2,60,0,1,0,1,1,1,1,1,0,0,1,1,0,1
> > >*  Column 0 = Measured Outcome or Class
> > >*  Column 1 = Age
> > >*  Column 2 = Number of exercise days per week
> > >*  Column 3 = Resting heart beat. 
> > >*  Rest are genome measures.         
>
> ### What is a Class ###
> > When using machine learning we take a set of rows where the outcome is known.  Each row represents the data from one patient,  One genome or one genomic run.  Each discrete outcome is considered class.
> >
> > Sample outcomes could be High Cancer Risk=0, Low cancer Risk = 1.    There must be at least two classes but there could be a larger number.  A general rule is more classes will require more training data to deliver good results.
> >
> > Choosing outcomes to be  measured is generally predicated on the desire to predict those outcomes using data where the answer is not known.  It is also the place where domain knowledge and intuition can help.    One of the hardest parts for many machine learning projects is gathering a sufficient amount of data that has been pre-classified to use for training. 
> >
> > Here are some example outcomes where each unique outcome represents a class. 
> >
> > > ##### Example simple outcomes:
> > > * class = 1 = Person had heart attack before Age of 40
> > > * class = 0 = Person did not have heart attack before 40. 
> > > ##### more complex set outcomes
> > > * class = 0 = Diagnosed Parkinsons Age 0 .. 20
> > > * class = 1 = Diagnosed Parkinsons Age 21 .. 40
> > > * Class = 2 = Diagnosed Parkinsons Age 41 .. 50
> > > * class = 3 = Diagnosed Parkinsons Age 51 .. 60
> > > * c lass = 4 = Diagnosed Parkinsons Age 61 .. 90        

>>In reality there can be any number up classes.  Keeping the number small tends to work somewhat better but there are applications such as ethnic origin that may require hundreds of classes. 
>>
>>Classes are always converted to a discrete set of integers for the use of the engine but they can be mapped back to strings to provide the literal interpretation as needed. 
>>
>>Any single classification request actually produces the probability for each class where there is some indication of a match.  For example if classifying based on ethnicity the actual answer may be 
>>
>>- 42% - Caucasian
>>- 18% - American Indian
>>- 12% - South Africa 
>>
>>This should not be thought of as a accurate percentage but rather a relative quality of the match.   It should not be used as true a probability output but you can safely use it to say the the match for Caucasian  42 / 18 = 2.3 times as good as the match for American Indian.  Even this can be a little dubious under some conditions.   It is safer to interpret the results as higher probability numbers are better matches than lower probability numbers but the actual amount of difference can be misleading unless you dig into the detailed math behind each prediction.  
>>
>>The engine generally selects the best match and reports on it but it is an option to return data on all matches. 
>## Choosing Input Data ##
>>Some of genome analysis tools are written with specific algorithms based on domain expertise.  Machine learning attempts to accomplish the same thing using pattern matching and statistics but it still helpful to have human experts who can identify the outcomes they want to measures and isolate portions of the genome.   Each different person becomes one row of data.   In some instances we directly consume the genomic data slice while in others we consume data produced by several other previous analysis tools.   
>>
>>Choosing which data to include or which tools to consume data from is a complex process but we do provide some tools that can help practitioners determine which data provides the greatest predictive value. 
>>
>>#### Granularity Feature Input Data
>>
>>> While input data like a Genomome measures individual data elements as a zero or one.  We can also use other data such as Age that may be a number between 0.0 and 150. In low dimensionality data such as zero or 1 0 it provides easy classification.   Other data such as age can grouping the data for similarity can provide better predictive output with less training data.  
>>>
>>> 1. 0..25 = young
>>> 2. 26..50=adult
>>> 3. 51..65=mature
>>> 4. 65..80=senior
>>> 5. 81-150=ancient. 
>>>
>>> Choosing the number of buckets is as much art as science and is covered in another topic.    In advanced systems the optimizer is allowed to select the group size while seeking to find best predictive output.     
>>>
>>> The basic Quantized classifier will accept a single number and based on requested number of groups it will divide the data evening between those groups.    Advanced optimizers are allowed to change the number of groups seeking to find the granularity that provides the best predictive output.  In some instances the granularity it chooses can be important data for the researcher because it may find that it yields best predives results when age is only divided into two buckets.
>>>
>>> In many cases previous analyis tools will generated data that is pre-grouped into a set similar to the example above where the researcher has already chosen a set of buckets.  This is transparently suppored by the classifier and it can even combine those buckets in the optimizer if it provides improved prediction acuracy. 
>>>
>>> In generall reducing the number of measurement risks reduce risk of over learning which is covered in another topic. 

>## Test Versus Learn Verus Runtime ##
>> The Data set is divided into discrete portions.  
>>
>> 1. One portion is  used for **training** the system.  
>> 2. The second set is used to **test** the systems ability to accurately classify outcomes  given a set of inputs.   
>> 3. A third set could real time inputs where we want to use the system to provide classification services. 
>>
>> When determining how well a machine learning engine is working we measure two  aspects
>>
>> precision which is if the system classifies a given row  is a member of a given class such as 1 = high risk for  X how often is it correct.    
>>
>> The second  Recall is of those who should have been classified as a member of a given class how many did it find. as   1 = high rist for X how many did it find.   
>>
>> There is always a balancing act between recall and precision.  Choosing what is most important can be a challenging decision. 
>>
>> -  Increasing precision will reduce recall 
>> -  Increasing recall will reduce precision.  

>> Optimizers are used in an attempt to increase either precision or recall while minimizing detrimental effect on the other.  A simple optimizer may vary the weight or important of individual features.   In some instances the the optimizer is allowed to vary the quant size or grouping used.     
>>
>> The output of the optimizer can yield information valuable to the researcher.  For example:  if the optimizer finds that it can provide the best prediction when the priority of the age input is turned up but only when it has been reduced to grouping into 3 groups then this can help the researcher know where to look. 
>>
>> There are many strategies for varying the selection of test verus training data but in general they try to find a compromise between the accuracy and recall of the engine so it will truely do the best job when asked to classify new data is has never seen previously.  A search on "avoid over learning in optimized machine learning" will yield a lot of information about this topic. 

># Genome Use of Optimizers #
>>Looking at the data below.  The slice of the genome use to supply columns c1 to c15 were selected by a researcher as a subset they thought could help predict or classify something.   The optimizer can help identify which bits are providing useful input.
>>     class,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15
>>     0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
>>     0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
>>     1,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
>>     0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
>>     1,0,1,0,1,0,1,1,1,0,0,0,0,1,1,
>>     0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
>>     
>>     class = 0 - not diagnosed with canser before age of 40.
>>     class = 1 = was diagnosed with cancer before age of 40.
>>
>>#### Identifying relevant portions of the Genome. 
>>
>> It is possible that bits C3,C11,C15 are very important for this diagnosis while bit C1 and C5 actually provide bad data while C6 is important but less important than C3.   If this information can identified then it can help the researcher identify which portion genome actually help and this can feed back to help them refine their diagnostic capabilty for future patients. 
>>
>> The optimizer is allowed to change 2 things.  
>>
>>- How important a given feature / columns is or weight
>>- How the column is grouped. 
>>
>> If a the system reduces the number of buckets it is causing more items to be clumped together.  In the genome context  reducing the number of buckets from 2 to 1 for a bit that has 2 possibilities  essentialy turns that bit off.   A similar approach of changing from  a decimal number like age from 3 buckets to 10 buckets allows age groups to be divided in to smaller groups providing more precision.  
>>
>> If the system changes the weight of a given feature up from 1.0 to 10.0 and it improves the quality of the classification then it means that feature is more important.  In contrast it can turn priority from one to 0.1 and have much less impact.  A priority of 0 would be  the same as a 1 bucket. 
>>
>> The combined set of these choices should give the researcher insight into their data that would be difficult to discover in other ways.
>>
>> ##### How the optimizer works
>>
>> In the most simplified approach the system is forced to choose the most accurate classification for each row which gives us 100% recall.  The system then seeks to improve precision of accuracy while retaining 100% recall.    In other situations the system is allowed to have recall drop to a specified threshold such as 90% while seeking to increase precision.   
>>
>> The general rule is if a change results in increased precision without reduced recall it can be kept.  If the change results in increased recall without a reduction in precision it can be kept.  If the change results in less complexity in the form of fewer quant buckets without reduced precision or recall it can be kept.   There are many variations of these rules.
>>
>> The changes made and the order of the changes is random.  Even so here are possibilities for getting trapped in local blind spots.    Eventually every optimization will stabilize where it an not find any more options.     One way to avoid local minimum is to keep the top 100 best set of optimization setting then randomly combine them for further testing.   Another way to avoid local optima is to randomly make some changes that are kept regardless of their impact then let the optimizer continue to run.    A preferred strategy is to use several different ways of selecting the test versus training data eg: run the optimizer with every 5th record from the training set first.  Then run it with every 4th record then run with randomly selected data.   Keep each of these results and either merge them into a combined set.   There are many ways to handle this. 
>>
>> ###### Overlearning
>>
>> One risk in optimized systems is that they can over learn where they become so specialized they can prediction with near 100% accuracy against the training and test data but when ran against new data their quality suffers.   A general rule is that the more features and more quanta buckets used the higher the risk of over learning.  This is balanced against the fact that more quanta buckets can be critical for good prediction in some contexts.      
>>
>> We seek to avoid over learning by encouraging the system to turn features off during the optimization process and by reducing the number of buckets.    Every time it chooses a random feature to change it first runs the test with that feature set to 1 quanta, Tests with 1/2 current number of quanta, Tests with 20% less quata and only then tests for the randomly chosen value.  If all tests return the same results then it will choose the one that reduces total number of quant buckets in the system.      A similar approach is used for feature priority where it is first tested with 0 priority and 1 priority before it is allowed to make the random priority change.  If all changes in priority yield the same results it will chose the one with the smallest delta between the value and 1.0
>>
>> We test for over learning by selecting different pieces of the training data for test. EG: select every 5th record for testing then select every 3rd record for training.  The engine is retrained with the rest of the data using the current sets so the training never sees the set currently selected for testing.   A well optimized system should maintain it's prediction accuracy  across several variations without needing to change the settings.  We also test against the formal test set but if we run that test and then run again it is a form of cheating. 
>
># Prepare Data #
>>  In a general system a set of data composed of 1..N rows comprised of 1..X columns is supplied.  This data is divided between Test and Training data.  The system is trained using the training data and then tested and optimized using the test data.    Once this process is complete the system is used to classify new data that it has never seen before.  If everything works well then it will do a good job of classifying that data.  The output could be consumed in a variety of reports or user interfaces. 
>>
>>  Example of Data set for predicting breast cancer:
>>
>>     Class,ClumpThick,UnifCellSize,UnifCellShape,margAdhesion,singleEpithelialCellSize,BareNucleo,BlandChromatin,NormalNucleoli,Mitoses
>>     2,5,1,1,1,2,1,3,1,1
>>     2,5,4,4,5,7,10,3,2,1
>>     2,3,1,1,1,2,2,3,1,1
>>     2,6,8,8,1,3,4,3,7,1
>>     2,4,1,1,3,2,1,3,1,1
>>     4,8,10,10,8,7,10,9,7,1
>>
>>     The first column is the class.  
>>       2 = Cancer not detected.
>>       4 = Cancer was detected.
>>
>>     The rest are results from measurements and 
>>     tests ran by the Cancer doctor.  Based on 
>>     this data set the Quantized classifier 
>>     was able to achive 96% accuracy of predition
>>     in the test data set. 
>>
>
>Example of Genome Data
>>     
    class,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15
    0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
    1,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
    0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
    0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
    1,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0
    1,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0


>>     The class is measured results 
>>     0 - did not detect cancer before age 40.
>>     1 - detected cancer before age 40.
>>
>>     The rest of the columns represent a slice
>>     of data extracted from the genome. 
>>     Or several slices collected into a single
>>     row.  In the Genome context we may expect
>>     hundreds or thousands of features.

>>For machine learning we would need at least 1K rows to attemp classification.    A more reasonable minimum would be 50 rows of which 40K are used for training and 10K are used for testing.    When used with Genomic data we may find that several million rows provide better classification effectiveness. 
>>
>>The engine should be able to learn from this and predict yes,no if you feed it the same sub region of the genome for each person.   
>>
>>Please send us data sets using the premise.  I would love to try them.  



#Genome Determine chromosones that are most important predictors#

> TODO:  Fill this in

# Basics of a Quantized Machine Learning Classifier

> TODO Fill this in 

# Binome Prediction when using output from several tools

> TODO: Fill This In

# 