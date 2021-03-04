#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd

import sklearn




df = pd.read_csv("BBC News Train.csv")



df['category_id'] = df['Category'].factorize()[0]




unique_category_df = df[['Category','category_id']].drop_duplicates().sort_values('category_id')



category_to_id = dict(unique_category_df.values)
id_to_category = dict(unique_category_df[['category_id','Category']].values)





from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(encoding = 'latin-1', stop_words = 'english', ngram_range = (1,2), min_df = 5, norm = 'l2', sublinear_tf = True)

features = tfidf.fit_transform(df.Text).toarray()


labels = df.category_id






from sklearn.feature_selection import chi2



for Category, category_id in sorted(category_to_id.items()) :
    
    # do chi analysis for all the items in this category
    features_chi2 = chi2(features, labels == category_id)
    
    # sorting the indices of features_chi2[0] - the chi-squared stats of each feature
    indices = np.argsort(features_chi2[0])
    
    # converting the indices to feature names
    feature_names = np.array(tfidf.get_feature_names())[indices]
    
    # listing single word features
    unigrams = [ v for v in feature_names if len(v.split(' ')) == 1]
    
    # listing 2-word features
    bigrams = [ v for v in feature_names if len(v.split(' ')) == 2]
    
   

from sklearn.manifold import TSNE

sample_size = int(len(features) * 0.3)
np.random.seed(0)

# randomly selecting 30% of the sample
indices = np.random.choice(range(len(features)), size = sample_size, replace= False)

# printing array of all projected features of 30% of the randomly chosen samples
projected_features = TSNE(n_components = 2, random_state = 0).fit_transform(features[indices])


# In[22]:


c_id = 0 # choosing a category
projected_features[(labels[indices] == c_id).values]




from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

model = LogisticRegression(random_state = 0)

X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size = 0.33, random_state =0)

model.fit(X_train, y_train)

y_pred_prob = model.predict_proba(X_test)
y_pred = model.predict(X_test)


# <b> Analysing predictions </b>

# In[28]:



model.fit(features, labels)




# texts = ["Hooli stock price soared after a dip in PiedPiper revenue growth.",
#          "Captain Tsubasa scores a magnificent goal for the Japanese team.",
#          "Merryweather mercenaries are sent on another mission, as government oversight groups call for new sanctions.",
#          "Beyoncé releases a new album, tops the charts in all of south-east Asia!",
#          "You won't guess what the latest trend in data analysis is!"]

# text_features = tfidf.transform(texts)
# predictions = model.predict(text_features)
# for text, predicted in zip(texts, predictions):
#     print('"{}"'.format(text))
#     print("  - Predicted as: '{}'".format(id_to_category[predicted]))
#     print("")
    






import os

test_df = pd.read_csv("BBC News Test.csv")




test_features = tfidf.transform(test_df.Text.tolist())

Y_pred = model.predict(test_features)

Y_pred




from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))







