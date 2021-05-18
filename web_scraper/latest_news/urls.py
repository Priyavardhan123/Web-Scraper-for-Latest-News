from django.contrib import admin
from django.urls import path
from latest_news import views
import time
import threading
import os
from web_scraper import settings
import web_scraper

urlpatterns = [
    path("home", views.index, name='home'),
    path("business", views.business, name='business'),
    path("tech", views.tech, name='tech'),
    path("sports", views.sports, name='sports'),
    path("entertainment", views.entertainment, name='entertainment'),
    path("politics", views.politics, name='politics'),
    path("shownews/<int:hrs>", views.oldnews, name='oldnews'),
    path("adminlogin", views.adminlogin, name='adminlogin'),
    path("login", views.login, name='login'),
    path("adminhome", views.adminhome, name='adminhome'),
    path("reported", views.reported, name='reported'),
    path("report", views.report, name='report'),
    path("delete_news", views.delete_news, name='delete_news'),
    path("logout", views.logout, name='logout'),
    path("search", views.search, name='search'),
    path("push_noti",views.push_noti, name='push_noti'),
    #path("demo_notif", views.demo_notif, name="notification_demo"),
    #path("send_notif", views.send_notif, name="send_notification")
]

def startup():
    threading.Timer(1200.0, startup).start()
    print("Fetching news..." , time.ctime(time.time()))
    os.system('python3 latest_news/fetch_news.py')

startup()