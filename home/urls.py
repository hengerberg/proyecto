from pipes import Template
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'home'
urlpatterns = [
    path('', IndexView.as_view(), name='dashboard'),
    
    
]