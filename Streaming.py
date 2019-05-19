#some not used. will delete later
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from string import punctuation
from sklearn import svm
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from nltk import ngrams
from itertools import chain
from wordcloud import WordCloud

#read data frame
odf = pd.read_csv('/Users/Gianina/Documents/MSc/spark/notebooks/bookdataGianinaNoDuplicates.csv', encoding = 'unicode_escape')
odf.head()

#merge review title and text into a single column 
import pandas as pd
odf['list']=odf[['review_title','review_text']].values.tolist()
odf['review_title+text']=odf['list'].apply(''.join)
print(odf)

#remove neutral reviews (ranked 3)
#define positive (1) and negative (0) class
df = odf[odf['review_score'] != 3]
X = df['review_title+text']
y_dict = {1:0, 2:0, 4:1, 5:1}
y = df['review_score'].map(y_dict)
df.head()
#X.head()
#y.head()

#logistic regression model on word count
#c = CountVectorizer(stop_words = ('the', 'in', 'read', 'pages', 'his', 'was', 'what','would', 'am', 'so', 'is', 'from', 'that', 'will', 'then', 'up', 'still', 'did', 'also', 'through', 'about', 'this', 'you', 'and', 'or', 'for', 'at', 'as', 'to','of', 'a', 'an', 'but', 'when', 'since', 'because'))
tfidf = TfidfVectorizer(stop_words = 'english')

def text_fit(X, y, model,clf_model,coef_show=1):
    
    X_c = model.fit_transform(X)
    print('# features: {}'.format(X_c.shape[1]))
    X_train, X_test, y_train, y_test = train_test_split(X_c, y, random_state=0)
    print('# train records: {}'.format(X_train.shape[0]))
    print('# test records: {}'.format(X_test.shape[0]))
    clf = clf_model.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    print ('Model Accuracy: {}'.format(acc))
    
    if coef_show == 1: 
        w = model.get_feature_names()
        coef = clf.coef_.tolist()[0]
        coeff_df = pd.DataFrame({'Word' : w, 'Coefficient' : coef})
        coeff_df = coeff_df.sort_values(['Coefficient', 'Word'], ascending=[0, 1])
        print('')
        print('-Top 20 positive-')
        print(coeff_df.head(20).to_string(index=False))
        print('')
        print('-Top 20 negative-')        
        print(coeff_df.tail(20).to_string(index=False))
    
    
text_fit(X, y, c, LogisticRegression())

#base line accuracy (predicting with majority class: positive)
text_fit(X, y, c, DummyClassifier(),0)

# logistic regression model on TFIDF
tfidf = TfidfVectorizer(stop_words = 'english')
text_fit(X, y, tfidf, LogisticRegression())

# logistic regression model on TFIDF with ngram
tfidf_n = TfidfVectorizer(ngram_range=(1,2),stop_words = 'english')
text_fit(X, y, tfidf_n, LogisticRegression())
