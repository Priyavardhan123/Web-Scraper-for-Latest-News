from django.contrib import admin
from django.urls import path
from latest_news import views

urlpatterns = [
    path("", views.index, name='home')
]
