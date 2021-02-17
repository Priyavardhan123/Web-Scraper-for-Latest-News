from django.contrib import admin
from django.urls import path
from latest_news import views

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
