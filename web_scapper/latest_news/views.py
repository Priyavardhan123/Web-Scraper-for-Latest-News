from django.shortcuts import render, HttpResponse
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from web_scapper.utils import get_MongoClient
import os
import pymongo
from datetime import datetime
import requests
from bs4 import BeautifulSoup

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
    
    weather_report = get_weather()

    return render(request, 'business.html',{'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six, 'weather_report' : weather_report}) 

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
        
    weather_report = get_weather()

    return render(request, 'tech.html', {'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six, 'weather_report' : weather_report}) 

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
    
    weather_report = get_weather()

    return render(request, 'sports.html', {'news_list' : news_list , 'last_three' : last_three, 'last_six': last_six, 'weather_report' : weather_report}) 

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
    for i in range(3):
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