from django.contrib import admin
from django.urls import path
from latest_news import views

urlpatterns = [
    path("home", views.index, name='home'),
    path("international", views.international, name='international'),
    path("national", views.national, name='national'),
    path("sports", views.sports, name='sports'),
    path("finance", views.finance, name='finance'),
    path("entertainment", views.entertainment, name='entertainment'),
    path("adminlogin", views.adminlogin, name='adminlogin'),
    path("login", views.login, name='login'),
    path("reported", views.reported, name='reported'),
    path("logout", views.logout, name='logout')
]