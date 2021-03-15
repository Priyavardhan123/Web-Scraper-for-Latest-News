from django.contrib import admin
from django.urls import path
from latest_news import views
import time
import threading
import os

urlpatterns = [
    path("home", views.index, name='home'),
    path("business", views.business, name='business'),
    path("tech", views.tech, name='tech'),
    path("sports", views.sports, name='sports'),
    path("entertainment", views.entertainment, name='entertainment'),
    path("politics", views.politics, name='politics'),
    path("adminlogin", views.adminlogin, name='adminlogin'),
    path("login", views.login, name='login'),
    path("reported", views.reported, name='reported'),
    path("logout", views.logout, name='logout')
]

def startup():
    threading.Timer(1200.0, startup).start()
    print("Fetching news..." , time.ctime(time.time()))
    os.system('python3 latest_news/fetch_news.py')

startup()
