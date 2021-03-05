from django.shortcuts import render, HttpResponse
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
#from web_scapper.utils import get_MongoClient
import os
import pymongo
from datetime import datetime
import requests
from bs4 import BeautifulSoup


import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn
from sklearn.feature_selection import chi2
from sklearn.manifold import TSNE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os
# Create your views here.

db_name = "web_scraper"
port = 27017
host = "localhost"
username = ""
password = ""
myclient = None


def get_MongoClient():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web-scraper"]
    return myclient, mydb

def get_weather():
    page1 = requests.get('https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather')
    soup1 = BeautifulSoup(page1.content, 'lxml')
    h = soup1.find("span", class_='BNeawe tAd8D AP7Wnd')
    city = str(h.text).split(",")[0]

    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=46c58e3eded12aaeb86c8287b19e4de5')
    weather_report = {}
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather_report['city'] = city
        weather_report['temp'] = int(main['feels_like'] - 273.15)
        weather_report['humidity'] = main['humidity']
        weather_report['weather'] = data['weather'][0]['description']
        weather_report['icon'] = data['weather'][0]['icon']
    
    return weather_report

def index(request):
    os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find()
    news_list = []
    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        news_list.append(i)

        # Delete news with duration more than 36 hrs(129600 seconds) 
        if duration>129600:              
            mycol.delete_one({'Headline' : i['Headline']})
    
    last_five = []
    for i in range(5):
        last_five.append(news_list.pop())
    
    last_eight = []
    for i in range(8):
        last_eight.append(news_list.pop())

    weather_report = get_weather()
            
    return render(request, 'index.html', {'news_list' : news_list , 'last_five' : last_five, 'last_eight' : last_eight, 'weather_report' : weather_report}) 
    
def business(request):
    # os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find({'Category' : 'business'})
    news_list = []
    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        news_list.append(i)

        # Delete news with duration more than 36 hrs(129600 seconds) 
        if duration>129600:              
            mycol.delete_one({'Headline' : i['Headline']})
    
    last_three = []
    if len(news_list)>3:
        for i in range(3):
            last_three.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_three.append(news_list.pop())

    last_six = []
    if len(news_list)>6:
        for i in range(6):
            last_six.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_six.append(news_list.pop())
    
    weather_report = get_weather()

    return render(request, 'business.html',{'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six, 'weather_report' : weather_report}) 

def tech(request):
    # os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find({'Category' : 'tech'})
    news_list = []
    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        news_list.append(i)

        # Delete news with duration more than 36 hrs(129600 seconds) 
        if duration>129600:              
            mycol.delete_one({'Headline' : i['Headline']})
    
    last_three = []
    if len(news_list)>3:
        for i in range(3):
            last_three.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_three.append(news_list.pop())

    last_six = []
    if len(news_list)>6:
        for i in range(6):
            last_six.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_six.append(news_list.pop())
        
    weather_report = get_weather()

    return render(request, 'tech.html', {'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six, 'weather_report' : weather_report}) 

def sports(request):
    # os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find({'Category' : 'sport'})
    news_list = []
    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        news_list.append(i)

        # Delete news with duration more than 36 hrs(129600 seconds) 
        if duration>129600:              
            mycol.delete_one({'Headline' : i['Headline']})
    
    last_three = []
    if len(news_list)>3:
        for i in range(3):
            last_three.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_three.append(news_list.pop())

    last_six = []
    if len(news_list)>6:
        for i in range(6):
            last_six.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_six.append(news_list.pop())
    
    weather_report = get_weather()

    return render(request, 'sports.html', {'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six, 'weather_report' : weather_report}) 

def entertainment(request):
    # os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find({'Category' : 'entertainment'})
    news_list = []
    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        news_list.append(i)

        # Delete news with duration more than 36 hrs(129600 seconds) 
        if duration>129600:              
            mycol.delete_one({'Headline' : i['Headline']})
    
    last_three = []
    if len(news_list)>3:
        for i in range(3):
            last_three.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_three.append(news_list.pop())

    last_six = []
    if len(news_list)>6:
        for i in range(6):
            last_six.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_six.append(news_list.pop())
    
    weather_report = get_weather()

    return render(request, 'entertainment.html', {'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six, 'weather_report' : weather_report}) 

def politics(request):
    # os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find({'Category' : 'Politics'})
    news_list = []
    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        news_list.append(i)

        # Delete news with duration more than 36 hrs(129600 seconds) 
        if duration>129600:              
            mycol.delete_one({'Headline' : i['Headline']})
    
    last_three = []
    if len(news_list)>3:
        for i in range(3):
            last_three.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_three.append(news_list.pop())

    last_six = []
    if len(news_list)>6:
        for i in range(6):
            last_six.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_six.append(news_list.pop())
    
    weather_report = get_weather()

    return render(request, 'politics.html', {'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six, 'weather_report' : weather_report}) 

def adminlogin(request):
    if not request.session.get('useremail', None):
        print("user is not logged in")
        c = {}
        c.update(csrf(request))
        return render(request, 'adminlogin.html', c)
    else:
        return HttpResponseRedirect('/reported')


def login(request):
    useremail = request.POST.get('useremail')
    password = request.POST.get('password')
    myclient, mydb = get_MongoClient()
    mycol = mydb["admin"]
    userobj = mycol.find_one({"useremail":useremail})
    # print(userobj]["password"])
    if userobj is None:
        return render(request, 'adminlogin.html', {'error':'Invalid Credentials!'})
    else:
        # print(userobj["password"])
        if password == userobj["password"]:
            request.session["useremail"] = useremail
            return HttpResponseRedirect('/reported')
        else:
            return render(request, 'adminlogin.html', {'error':'Invalid Credential!'})
    return render(request, 'adminlogin.html')

def logout(request):
    del request.session['useremail']
    return HttpResponseRedirect('/adminlogin')

def reported(request):
    if not request.session.get('useremail', None):
        print("user is not logged in")
        c = {}
        c.update(csrf(request))
        return render(request, 'adminlogin.html', c)
    else:
        return render(request, 'reported.html') 

def category(texts):
    df = pd.read_csv("latest_news/BBC News Train.csv")
    df['category_id'] = df['Category'].factorize()[0]
    unique_category_df = df[['Category','category_id']].drop_duplicates().sort_values('category_id')
    category_to_id = dict(unique_category_df.values)
    id_to_category = dict(unique_category_df[['category_id','Category']].values)
    tfidf = TfidfVectorizer(encoding = 'latin-1', stop_words = 'english', ngram_range = (1,2), min_df = 5, norm = 'l2', sublinear_tf = True)
    features = tfidf.fit_transform(df.Text).toarray()
    labels = df.category_id

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

    sample_size = int(len(features) * 0.3)
    np.random.seed(0)

    # randomly selecting 30% of the sample
    indices = np.random.choice(range(len(features)), size = sample_size, replace= False)

    # printing array of all projected features of 30% of the randomly chosen samples
    projected_features = TSNE(n_components = 2, random_state = 0).fit_transform(features[indices])
    c_id = 0 # choosing a category
    projected_features[(labels[indices] == c_id).values]

    model = LogisticRegression(random_state = 0)

    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size = 0.33, random_state =0)

    model.fit(X_train, y_train)

    y_pred_prob = model.predict_proba(X_test)
    y_pred = model.predict(X_test)

    model.fit(features, labels)

    test_df = pd.read_csv("latest_news/BBC News Test.csv")

    test_features = tfidf.transform(test_df.Text.tolist())

    Y_pred = model.predict(test_features)

    text_features = tfidf.transform(texts)
    predictions = model.predict(text_features)
    prediction_list = []
    for text, predicted in zip(texts, predictions):
        # print('"{}"'.format(text))
        # print("  - Predicted as: '{}'".format(id_to_category[predicted]))
        # print("")
        prediction_list.append((id_to_category[predicted]))

    return prediction_list