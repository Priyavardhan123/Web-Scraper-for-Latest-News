from django.shortcuts import render, HttpResponse
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from web_scapper.utils import get_MongoClient
import os
import pymongo
from datetime import datetime

# Create your views here.
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
            
    return render(request, 'index.html', {'news_list' : news_list , 'last_five' : last_five, 'last_eight' : last_eight}) 
    
def business(request):
    # os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find({'Category' : 'Business'})
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
    for i in range(3):
        last_three.append(news_list.pop())

    last_six = []
    if len(news_list)>6:
        for i in range(6):
            last_six.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_six.append(news_list.pop())
    
    return render(request, 'business.html',{'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six}) 

def tech(request):
    # os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find({'Category' : 'Tech'})
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
    for i in range(3):
        last_three.append(news_list.pop())

    last_six = []
    if len(news_list)>6:
        for i in range(6):
            last_six.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_six.append(news_list.pop())
    
    return render(request, 'tech.html', {'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six}) 

def sports(request):
    # os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find({'Category' : 'Sports'})
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
    for i in range(3):
        last_three.append(news_list.pop())

    last_six = []
    if len(news_list)>6:
        for i in range(6):
            last_six.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_six.append(news_list.pop())
    
    return render(request, 'sports.html', {'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six}) 

def finance(request):
    return render(request, 'finance.html') 

def entertainment(request):
    # os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find({'Category' : 'Entertainment'})
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
    for i in range(3):
        last_three.append(news_list.pop())

    last_six = []
    if len(news_list)>6:
        for i in range(6):
            last_six.append(news_list.pop())
    else:
        for i in range(len(news_list)):
            last_six.append(news_list.pop())
    
    return render(request, 'entertainment.html', {'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six}) 

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