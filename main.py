# -*- coding: utf-8 -*-
"""FINAL CODE FOR PROJECT WITH OUTPUT_Take 9_FINAL-DON'T CHANGE- to show with manual testing-checkpoint.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18x8A3SzBncBhUP1giOfBAKKer8PX5de9

# Fake News Detection using Machine Learning
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""## Dataset creation"""

True_news = pd.read_csv('True.csv')
Fake_news = pd.read_csv('Fake.csv')

True_news['label']=1
Fake_news['label']=0
True_news['text']=True_news['text']+True_news['title']
Fake_news['text']=Fake_news['text']+Fake_news['title']

True_news.head()

Fake_news.head()

True_news.shape, Fake_news.shape

data1=True_news[['text','label']]
data2=Fake_news[['text','label']]
dataset=pd.concat([data1,data2])

dataset.shape

dataset.isnull().sum()

dataset['label'].value_counts()

data1.shape, data2.shape

dataset=dataset.sample(frac=1)

dataset.head(25)

dataset['text']

"""## Pre-processing of data"""

import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lem=WordNetLemmatizer()

stopwords=stopwords.words('english')

stopwords.extend(["reuters","via","image","http","twitter","com","www","getty"])

print(stopwords)

nltk.download('wordnet')

def cleaning_data(row):

    row = row.lower()
    row = re.sub('[^a-zA-Z]' , ' ' , row)
    row = re.sub('https?://\S+|www\.\S+', '', row)
    row = re.sub(r'http\S+','',row)
    token = nltk.word_tokenize(row)  ## edit 1
    news = [lem.lemmatize(word) for word in token if not word in stopwords]
    clean_news = ' '.join(news)
    return clean_news

dataset['text'] = dataset['text'].apply(lambda x : cleaning_data(x))

dataset.isnull().sum()

dataset.head()

dataset['text']

dataset.shape

"""### Adding extra data to dataset (old train set)"""

old_data=pd.read_csv('train.csv')
old_data=old_data[['title','text','label']]

old_data

old_data['text']=old_data['text']+old_data['title']

old_data.isnull().sum() #Checking for null values

old_data.dropna(axis=0, how="any", thresh=None, subset=['text','label','title'], inplace=True) #Removing null values

old_data.isnull().sum() #Checking for null values

old_data['text']=old_data['text'].apply((lambda x : cleaning_data(x)))## Cleaning data

old_data.shape

"""### Adding archive data to dataset"""

archive_data=pd.read_csv('news_archive2.csv')
archive_data=archive_data[['title','text','label']]
archive_data

archive_data['text']=archive_data['text']+archive_data['title']

archive_data.isnull().sum()#Checking for null values

archive_data.dropna(axis=0, how="any", thresh=None, subset=['text','label'], inplace=True)#Removing null values

archive_data.isnull().sum() #Checking for null values

archive_data['text']=archive_data['text'].apply((lambda x : cleaning_data(x)))## Cleaning data

archive_data.shape

"""## Combining 3 datasets"""

comb_data=pd.concat([dataset,old_data,archive_data])
comb_data=comb_data.sample(frac=1)
comb_data=comb_data[['text','label']]
comb_data

manual_test=comb_data.iloc[69045:69065]
manual_test

comb_data=comb_data[0:69045]
comb_data

"""## Train and Test Data"""

X = comb_data['text']
y = comb_data['label']

X.head()

y.head()

from sklearn.model_selection import train_test_split
train_data , test_data , train_label , test_label = train_test_split(X , y , test_size = 0.20 ,random_state = 0)

train_data.shape, test_data.shape

real_words = ''
fake_words = ''
for i in range(len(train_data)):
    txt=train_data.iloc[i]
    if train_label.iloc[i]==1:
        tokensr = txt.split()
        real_words += " ".join(tokensr)+" "

    else:
        tokensf=txt.split()
        fake_words += " ".join(tokensf)+" "

for i in range(len(test_data)):
    txt=test_data.iloc[i]
    if test_label.iloc[i]==1:
        tokensr = txt.split()
        real_words += " ".join(tokensr)+" "

    else:
        tokensf=txt.split()
        fake_words += " ".join(tokensf)+" "

"""### Word Cloud"""

from wordcloud import WordCloud

wordcloud = WordCloud(width = 800, height = 800,
                min_font_size = 10, max_words=80).generate(real_words)
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()

wordcloud = WordCloud(width = 800, height = 800,
                min_font_size = 10, max_words=80).generate(fake_words)
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()

"""## Applying TF-IDF vectorizer"""

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer=TfidfVectorizer(min_df=0.001,ngram_range=(1,2))

vec_train_data = vectorizer.fit_transform(train_data) #fitting and transforming vectorizer to train data

vec_test_data = vectorizer.transform(test_data) #transform test data

vec_train_data.shape , vec_test_data.shape #output:(no of news articles, number of features)

train_label.value_counts() #Checking if train and test data and comparable distribution of fake and real news

test_label.value_counts()

# creating of dictionary of feature names and respective idf values
#idf_dict=dict(zip(vectorizer.get_feature_names(),vectorizer.idf_))

# creating of dictionary of feature names and respective idf values
df_idf = pd.DataFrame(vectorizer.idf_, index=vectorizer.get_feature_names(),columns=["idf_weights"])
idf_least=df_idf.sort_values(by=['idf_weights']) # sort ascending - words with least idf values
idf_least

# idf_dict

idf_most=df_idf.sort_values(by=['idf_weights'],ascending=False) #sort descending - words with most idf weight
idf_most

df_tfidf1 = pd.DataFrame(vec_train_data[1].T.todense(), index=vectorizer.get_feature_names(), columns=["tfidf"])
df_tfidf1.sort_values(by=["tfidf"],ascending=False).iloc[0:30] #checking tf-idf values of a news in training set

print(vectorizer.vocabulary_) #vocabulary of vectorizer

"""## 1. Multinomial Naive Bayes - using"""

from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import accuracy_score,classification_report, confusion_matrix, roc_auc_score, precision_score, recall_score, f1_score

from sklearn.metrics import mean_squared_error

NB = MultinomialNB()

NB.fit(vec_train_data, train_label) #fitting model to train data
pred_NB  = NB.predict(vec_test_data)

print(classification_report(test_label , pred_NB))

#precision_score(test_label,pred_NB,pos_label=0),precision_score(test_label,pred_NB,pos_label=1)

pred_NB_train = NB.predict(vec_train_data)
print(classification_report(train_label , pred_NB_train))

accuracy_score(train_label , pred_NB_train), accuracy_score(test_label , pred_NB)

roc_auc_score(train_label,pred_NB_train),roc_auc_score(test_label,pred_NB)

NB.score(vec_train_data,train_label),NB.score(vec_test_data,test_label)

(mean_squared_error(test_label,pred_NB,squared=False))

confusion_matrix(test_label, pred_NB)

confusion_matrix(train_label, pred_NB_train)

prob_NB=pd.DataFrame(NB.predict_proba(vec_test_data))
prob_NB #probability for testing data

train_prob_NB=pd.DataFrame(NB.predict_proba(vec_train_data))

#Number of times token appears in each True article
true_token = NB.feature_count_[1, :]

#Number of times token appears in each Fake article
fake_token = NB.feature_count_[0, :]

true_token

tokens = pd.DataFrame({'token':vectorizer.get_feature_names(), 'true':true_token, 'fake':fake_token}).set_index('token')
tokens_t=tokens.sort_values(by=["true"],ascending=False).iloc[0:10]
tokens_t

tokens_f=tokens.sort_values(by=["fake"],ascending=False).iloc[0:10]
tokens_f

# add 1 to true and fake counts to avoid dividing by 0
tokens['true'] = tokens.true + 1
tokens['fake'] = tokens.fake + 1

# convert the true and fake counts into frequencies
tokens['true'] = tokens.true / NB.class_count_[0]
tokens['fake'] = tokens.fake / NB.class_count_[1]

# calculate the ratio of fake to true for each token
tokens['fake/true ratio'] = tokens.fake / tokens.true
most_fake=tokens.sort_values('fake/true ratio', ascending=False)

most_real=tokens.sort_values('fake/true ratio', ascending=True)

most_real.head(20) #most real words

most_fake.head(20) #most fake words

NB.coef_

"""## 2. Logistic Regression - using"""

from sklearn.linear_model import LogisticRegression

LR=LogisticRegression()
LR.fit(vec_train_data,train_label)

pred_LR=LR.predict(vec_test_data)

print(classification_report(test_label,pred_LR))

pred_LR_train = LR.predict(vec_train_data)
print(classification_report(train_label , pred_LR_train))

accuracy_score(train_label , pred_LR_train)

accuracy_score(test_label, pred_LR)

roc_auc_score(train_label,pred_LR_train),roc_auc_score(test_label,pred_LR)

LR.score(vec_train_data,train_label),LR.score(vec_test_data,test_label)

confusion_matrix(test_label, pred_LR)

confusion_matrix(train_label, pred_LR_train)

prob_LR=pd.DataFrame(LR.predict_proba(vec_test_data))
prob_LR

pd.DataFrame(LR.predict_proba(vec_train_data))

LR.coef_

LR.intercept_

"""## 3. LinearSVC sqaured hinge loss - using"""

from sklearn.svm import LinearSVC

SVCl= LinearSVC()

SVCl.fit(vec_train_data,train_label)

pred_SVCl=SVCl.predict(vec_test_data)

pred_SVCl_train = SVCl.predict(vec_train_data)
print(classification_report(train_label , pred_SVCl_train))

precision_score(train_label,pred_SVCl_train,pos_label=0),precision_score(train_label,pred_SVCl_train,pos_label=1)

SVCl.score(vec_train_data,train_label),SVCl.score(vec_test_data,test_label)

roc_auc_score(train_label,pred_SVCl_train),roc_auc_score(test_label,pred_SVCl)

print(classification_report(test_label,pred_SVCl))

precision_score(test_label,pred_SVCl,pos_label=0),precision_score(test_label,pred_SVCl,pos_label=1)

confusion_matrix(test_label, pred_SVCl)

confusion_matrix(train_label, pred_SVCl_train)

"""## SGD with SVM - not using"""

from sklearn.linear_model import SGDClassifier

SGD=SGDClassifier()
SGD.fit(vec_train_data,train_label)

pred_SGD=SGD.predict(vec_test_data)

pred_SGD_train = SGD.predict(vec_train_data)
print(classification_report(train_label , pred_SGD_train))

precision_score(test_label,pred_SGD,pos_label=0),precision_score(test_label,pred_SGD,pos_label=1)

accuracy_score(train_label , pred_SGD_train)

accuracy_score(test_label, pred_SGD)

SGD.score(vec_train_data,train_label),SGD.score(vec_test_data,test_label)

print(classification_report(test_label,pred_SGD))

confusion_matrix(test_label, pred_SGD)

confusion_matrix(train_label, pred_SGD_train)

"""## SGD with LR - not using"""

from sklearn.linear_model import SGDClassifier

SGDlr=SGDClassifier(loss='log')
SGDlr.fit(vec_train_data,train_label)

pred_SGDlr=SGDlr.predict(vec_test_data)

pred_SGDlr_train = SGDlr.predict(vec_train_data)
print(classification_report(train_label , pred_SGDlr_train))

accuracy_score(train_label , pred_SGDlr_train)

accuracy_score(test_label, pred_SGDlr)

SGDlr.score(vec_train_data,train_label),SGDlr.score(vec_test_data,test_label)

print(classification_report(test_label,pred_SGDlr))

confusion_matrix(test_label, pred_SGDlr)

confusion_matrix(train_label, pred_SGDlr_train)

"""## Saving the model"""

import joblib

joblib.dump(vectorizer,'v9.sav')

joblib.dump(NB,'modelNB9.sav')

joblib.dump(LR,'modelLR9.sav')

joblib.dump(SVCl,'modelSVC9.sav')

joblib.dump(SGDlr,'modelSGDlr9.sav')

joblib.dump(SGD,'modelSGDsvm9.sav')

from sklearn.pipeline import Pipeline

pipe = Pipeline([('tfidf', vectorizer),('clf', NB)])

joblib.dump(pipe,'pipeline.sav')

"""## Manual Testing"""

model_nb=joblib.load('modelNB9.sav')
model_lr=joblib.load('modelLR9.sav')
model_svc=joblib.load('modelSVC9.sav')
v=joblib.load('v.sav')

trialdata=[]

trialdata2=[]

i=6
label_t=manual_test['label'].iloc[i]
label_t

news=manual_test['text'].iloc[i]
news

news=input()
label_t=0
# label_t=int(input('Given label '))
model_test={'text':[news]}
new_test=pd.DataFrame(model_test)
new_test['text']=new_test['text'].apply((lambda x : cleaning_data(x)))
new_test_data=new_test['text']
new_vec_test=vectorizer.transform(new_test_data)
nb_p=model_nb.predict(new_vec_test)
lr_p=model_lr.predict(new_vec_test)
svc_p=model_svc.predict(new_vec_test)

prob=pd.DataFrame(model_nb.predict_proba(new_vec_test))

print('\nNB Prediction: \n')
print('{}% REAL \n{}% FAKE'.format(round(prob[1].iloc[0]*100,2),round(prob[0].iloc[0]*100,2)))
print('given label: ',label_t)
print('predicted label: ',nb_p[0])
if label_t==nb_p[0]:
    print('Prediction is Correct')
else: print('Prediction is not correct')

prob2=pd.DataFrame(model_lr.predict_proba(new_vec_test))

print('\nLR Prediction: \n')
print('{}% REAL \n{}% FAKE'.format(round(prob2[1].iloc[0]*100,2),round(prob2[0].iloc[0]*100,2)))
print('given label: ',label_t)
print('predicted label: ',lr_p[0])
if label_t==lr_p[0]:
    print('Prediction is Correct')
else: print('Prediction is not correct')

print('\nSVM Prediction: ',svc_p[0])
if label_t==svc_p[0]:
    print('Prediction is Correct')
else: print('Prediction is not correct')

trialdata.append([new_test_data.iloc[0],label_t,round(prob[1].iloc[0]*100,2),round(prob[0].iloc[0]*100,2),nb_p[0],round(prob2[1].iloc[0]*100,2),round(prob2[0].iloc[0]*100,2),lr_p[0],svc_p[0]])

trial_test=pd.DataFrame(trialdata,columns=['cleaned data','label','nb real','nb fake','nb pred','lr real','lr fake','lr pred','svm pred'])

trial_test

news=input()
# label_t=int(input('Given label '))
label_t=1
model_test={'text':[news]}
new_test=pd.DataFrame(model_test)
new_test['text']=new_test['text'].apply((lambda x : cleaning_data(x)))
new_test_data=new_test['text']
new_vec_test=vectorizer.transform(new_test_data)
nb_p=model_nb.predict(new_vec_test)
lr_p=model_lr.predict(new_vec_test)
svc_p=model_svc.predict(new_vec_test)

prob=pd.DataFrame(model_nb.predict_proba(new_vec_test))

print('\nNB Prediction: \n')
print('{}% REAL \n{}% FAKE'.format(round(prob[1].iloc[0]*100,2),round(prob[0].iloc[0]*100,2)))
print('given label: ',label_t)
print('predicted label: ',nb_p[0])
if label_t==nb_p[0]:
    print('Prediction is Correct')
else: print('Prediction is not correct')

prob2=pd.DataFrame(model_lr.predict_proba(new_vec_test))

print('\nLR Prediction: \n')
print('{}% REAL \n{}% FAKE'.format(round(prob2[1].iloc[0]*100,2),round(prob2[0].iloc[0]*100,2)))
print('given label: ',label_t)
print('predicted label: ',lr_p[0])
if label_t==lr_p[0]:
    print('Prediction is Correct')
else: print('Prediction is not correct')

print('\nSVM Prediction: ',svc_p[0])
if label_t==svc_p[0]:
    print('Prediction is Correct')
else: print('Prediction is not correct')

trialdata2.append([new_test_data.iloc[0],label_t,round(prob[1].iloc[0]*100,2),round(prob[0].iloc[0]*100,2),nb_p[0],round(prob2[1].iloc[0]*100,2),round(prob2[0].iloc[0]*100,2),lr_p[0],svc_p[0]])

trial_test2=pd.DataFrame(trialdata2,columns=['cleaned data','label','nb real','nb fake','nb pred','lr real','lr fake','lr pred','svm pred'])

trial_test2

df_manual=pd.DataFrame(new_vec_test.toarray(),columns=vectorizer.get_feature_names())
df_manual

df_tfidf1 = pd.DataFrame(new_vec_test[0].T.todense(), index=vectorizer.get_feature_names(), columns=["tfidf"])
df_tfidf1.sort_values(by=["tfidf"],ascending=False).iloc[0:30]

df_tfidf0 = pd.DataFrame(new_vec_test[0].T.todense(), index=vectorizer.get_feature_names(), columns=["tfidf"])
df_tfidf0.sort_values(by=["tfidf"],ascending=False).iloc[0:30]

df_labels=pd.DataFrame(test_label)

df_labels['nb pred']=pred_NB

df_labels['lr pred']=pred_LR

df_labels['svc pred']=pred_SVCl

df_labels