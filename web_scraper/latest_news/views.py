from django.shortcuts import render, HttpResponse
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
import os
import pymongo
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bson import ObjectId
import time
import threading

#Push Notification imports
from webpush import send_user_notification
from webpush import send_group_notification

#ML Model imports
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn
from sklearn.feature_selection import chi2
from sklearn.manifold import TSNE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os

login_error = "Invalid Credentials!"

db_name = "web_scraper"
port = 27017
host = "localhost"
username = ""
password = ""
myclient = None

# Create your views here.

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
        i['id'] = i['_id']
        news_list.append(i)

        # Delete news with duration more than 36 hrs(129600 seconds) 
        if duration>129600:              
            mycol.delete_one({'Headline' : i['Headline']})
    
    last_five = []
    for i in range(5):
        last_five.append(news_list.pop())
    
    #Sending Push Notification
    head = last_five[0]['Headline']
    body = last_five[0]['Content']
    send_pn(head, body)
    
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
        i['id'] = i['_id']
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
        i['id'] = i['_id']
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
        i['id'] = i['_id']
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
        i['id'] = i['_id']
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

    news = mycol.find({'Category' : 'politics'})
    news_list = []
    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        i['id'] = i['_id']
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
        return HttpResponseRedirect('/adminhome')
    
@require_POST
def login(request):
    useremail = request.POST.get('useremail')
    password = request.POST.get('password')
    myclient, mydb = get_MongoClient()
    mycol = mydb["admin"]
    userobj = mycol.find_one({"useremail":useremail})
    # print(userobj]["password"])
    if userobj is None:
        return render(request, 'adminlogin.html', {'error':login_error})
    else:
        # print(userobj["password"])
        if password == userobj["password"]:
            request.session["useremail"] = useremail
            return HttpResponseRedirect('/adminhome')
        else:
            return render(request, 'adminlogin.html', {'error':login_error})
    return render(request, 'adminlogin.html')

def logout(request):
    del request.session['useremail']
    return HttpResponseRedirect('/adminlogin')

# All news page for Admin
def adminhome(request):
    if not request.session.get('useremail', None):
        print("user is not logged in")
        c = {}
        c.update(csrf(request))
        return render(request, 'adminlogin.html', c)

    c = {}
    c.update(csrf(request))
    #Getting news list from database
    myclient, mydb = get_MongoClient()
    mycol = mydb["news_table"]

    news = mycol.find()
    news_list = []
    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        #Setting the duration
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        i['id'] = i['_id']
        news_list.append(i)
    
    page = request.GET.get('page', 1)

    #Django Pagination
    paginator = Paginator(news_list, 10)

    try:
        news = paginator.page(page)
    
    #For first page
    except PageNotAnInteger:
        news = paginator.page(1)

    #For last page
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'adminhome.html', {"news" : news})

# Reported News page for admin
def reported(request):
    if not request.session.get('useremail', None):
        print("user is not logged in")
        c = {}
        c.update(csrf(request))
        return render(request, 'adminlogin.html', c)

    #Getting news list from database
    c = {}
    c.update(csrf(request))
    myclient, mydb = get_MongoClient()
    mycol = mydb["news_table"]

    news = mycol.find({'Reported' : True})
    news_list = []

    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        #Setting the duration
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        i['id'] = i['_id']
        news_list.append(i)

    nl_len = len(news_list)

    page = request.GET.get('page', 1)

    #Django Pagination
    paginator = Paginator(news_list, 10)

    try:
        news = paginator.page(page)
    
    #For first page
    except PageNotAnInteger:
        news = paginator.page(1)

    #For last page
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'reported.html', {"news" : news, "nl_len" : nl_len})

# Showing news of past x hrs
def oldnews(request, hrs):

    #Getting news list from database
    c = {}
    c.update(csrf(request))
    myclient, mydb = get_MongoClient()
    mycol = mydb["news_table"]

    news = mycol.find()
    news_list = []

    for i in news:
        time = i['DateTime']
        current_time = datetime.now()
        #Setting the duration
        duration = (current_time - time).total_seconds()
        i['DateTime'] = int(duration//60)
        i['id'] = i['_id']

        # Keeping news which were latest by 6 hrs (21600 sec)
        if(duration < (hrs * 3600)):
            news_list.append(i)

    nl_len = len(news_list)

    page = request.GET.get('page', 1)

    #Django Pagination
    paginator = Paginator(news_list, 10)

    try:
        news = paginator.page(page)
    
    #For first page
    except PageNotAnInteger:
        news = paginator.page(1)

    #For last page
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    weather_report = get_weather()
    return render(request, 'shownews.html', {"news" : news, "nl_len" : nl_len, 'weather_report' : weather_report})

@require_POST
def delete_news(request):
    if not request.session.get('useremail', None):
        print("user is not logged in")
        c = {}
        c.update(csrf(request))
        return render(request, 'adminlogin.html', c)

    #Deleting news from database
    myclient, mydb = get_MongoClient()
    mycol = mydb["news_table"]
    id = request.POST.get('newsid')
    mycol.delete_one({'_id' : ObjectId(id)})
    print("\n-------News Id : ",id, "deleted successfully!--------\n")

    return HttpResponseRedirect('/adminhome')

@require_POST
def report(request):
    # Updating 'reported' field of news in database
    myclient, mydb = get_MongoClient()
    mycol = mydb["news_table"]
    id = request.POST.get('newsid')
    myquery = { "_id": ObjectId(id)}
    newvalues = { "$set": { "Reported": True } }
    mycol.update_one(myquery, newvalues)
    print("\n-------News Id : ",id, "reported successfully!--------\n")

    return HttpResponseRedirect("/home")

# Searching News
@require_POST
def search(request):

    # Getting Search query
    query = request.POST.get('squery')
    # For null query
    if query is None:
        return HttpResponseRedirect("/home")

    myclient, mydb = get_MongoClient()
    mycol = mydb["news_table"]

    # Using MongoDB's Text index for searching on Headline, Content, Category and Source fields
    news = mycol.find({"$text" : {"$search" : query}})
    news_list = []

    for i in news:
        news_list.append(i)
    nl_len = len(news_list)
    weather_report = get_weather()
    return render(request, 'search.html', {"news" : news_list, "nl_len" : nl_len, 'weather_report' : weather_report})
    
def push_noti(request):
    webpush = {"group": "all"}
    return render(request, 'notification.html', {"webpush" : webpush})

def demo_notif(request):
    return render(request,'demoNotif.html')

@require_POST
def send_notif(request):
    head = request.POST.get('head')
    body = request.POST.get('body')
    send_pn(head, body)
    return HttpResponseRedirect('/demo_notif')


#ML Algorithm for finding category of news
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

#Getting mongoDb access
def get_MongoClient():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    return myclient, mydb

#Sending push notification
def send_pn(head, body):
    payload = {"head": head, "body": body, "icon": "/static/images/notification.png", "url": "http://127.0.0.1:8000/home"}
    try:
        send_group_notification(group_name="all", payload=payload, ttl=1000)
    except Exception as e:
        print(e)


