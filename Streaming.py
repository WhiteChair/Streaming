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
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
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
odf['review_title_text'] = odf.agg('{0[review_title]}  {0[review_text]}'.format, axis=1)

#odf['list']=odf[['review_title','review_text']].values.tolist()
#odf['review_title_text']=odf['list'].apply(''.join)

print(odf)

#remove neutral reviews (ranked 3)
#define positive (1) and negative (0) class
df = odf[odf['review_score'] != 3]
X = df['review_title_text']
y_dict = {1:0, 2:0, 4:1, 5:1}
y = df['review_score'].map(y_dict)
df.head()
#X.head()
#y.head()

#logistic regression model on word count
c = CountVectorizer(stop_words = ('the', 'in', 'read', 'pages', 'his', 'was', 'what','would', 'am', 'so', 'is', 'from', 'that', 'will', 'then', 'up', 'still', 'did', 'also', 'through', 'about', 'this', 'you', 'and', 'or', 'for', 'at', 'as', 'to','of', 'a', 'an', 'but', 'when', 'since', 'because'))
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

frames = [X, y]
df2 = pd.concat(frames, axis=1)
df2.head(5)

#split into training-validation for NB
ns_train, ns_test = train_test_split(df2, test_size=0.3)
ns_train.head(5)
ns_test.head(5)

#Naive Bayes
vectorizer = TfidfVectorizer()

ns_train_matrix = vectorizer.fit_transform(ns_train.review_title_text)
ns_train_label = ns_train.review_score
ns_test_matrix = vectorizer.transform(ns_test.review_title_text)
ns_test_label = ns_test.review_score

clf = MultinomialNB()
clf.fit(ns_train_matrix, ns_train_label)

ns_pred = clf.predict(ns_test_matrix)
ns_acc = accuracy_score(ns_test_label, ns_pred)
ns_f1 = f1_score(ns_test_label, ns_pred)
ns_prec = precision_score(ns_test_label, ns_pred)
ns_rec = recall_score(ns_test_label, ns_pred)

print('Accuracy: {0:.2f}%'.format(ns_acc*100))
print('Precision Score: {0:.2f}%'.format(ns_prec*100))
print('Recall Score: {0:.2f}%'.format(ns_rec*100))
print('F1 Score: {0:.4f}'.format(ns_f1))
