from django.shortcuts import render, HttpResponse
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from web_scapper.utils import get_MongoClient
import os
import pymongo

# Create your views here.
def index(request):
    os.system('python3 latest_news/fetch_news.py')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["web_scraper"]
    mycol = mydb["news_table"]

    news = mycol.find()
    news_list = []
    for i in news:
        news_list.append(i)
    
    last_five = []
    for i in range(5):
        last_five.append(news_list.pop())
    
    last_eight = []
    for i in range(8):
        last_eight.append(news_list.pop())
    
    # print(last_five)
        
    return render(request, 'index.html', {'news_list' : news_list , 'last_five' : last_five, 'last_eight' : last_eight}) 
    
def international(request):
    return render(request, 'international.html') 

def national(request):
    return render(request, 'national.html') 

def sports(request):
    return render(request, 'sports.html') 

def finance(request):
    return render(request, 'finance.html') 

def entertainment(request):
    return render(request, 'entertainment.html')

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