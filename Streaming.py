#!/usr/bin/env python
# coding: utf-8

# In[54]:


import pyspark
from pyspark.sql import functions as sf
from pyspark import SparkContext


# In[55]:


#Read static .csv
from pyspark.sql import SQLContext
sqlContext=SQLContext(sc)
df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('bookdataGianinaNoDuplicates.csv')
df.show(5)


# In[56]:


#merge review title and text into a single column for analysis
df2=df.withColumn('review_title+review_text', sf.concat(sf.col('review_text'), sf.lit (' '), sf.col('review_title')))
df2.show(5)


# In[58]:


#drop NA's
df3=df2.dropna(how="any")
df3.show(5)


# In[43]:


#split into training and test datasets
(bookdatatrain, bookdatatest)=df3.randomSplit([0.8, 0.2], seed=100)


# In[46]:


#text pre-processing - removing operators. could not get it to work
import re
REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_bookdata(df3.review_title+review_text):
    df3.review_title+review_text = [REPLACE_NO_SPACE.sub("", line.lower()) for line in df3.review_title+review_text]
    df3.review_title+review_text = [REPLACE_WITH_SPACE.sub(" ", line) for line in df3.review_title+review_text] 
    return df3.review_title+review_text

bookdatatrain_clean = preprocess_bookdata(bookdatatrain)
bookdatatest_clean = preprocess_bookdata(bookdatatest)


# In[59]:


#text pre-processing
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
rt=RegexTokenizer(inputCol="review_title+review_text", outputCol="words", pattern="//W")
add_stopwords=['the', 'and', 'or', 'at', 'as', 'to','of', 'a', 'an'] #add more
swr=StopWordsRemover(inputCol="words",outputCol="filtered").setStopWords(add_stopwords)
cv=CountVectorizer(inputCol="filtered",outputCol="features", vocabSize=10000, minDF=3)

