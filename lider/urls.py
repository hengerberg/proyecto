from pipes import Template
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'lider'
urlpatterns = [
    path('', IndexView.as_view(), name='inicio'),
    path('supervisor/add', SupervisorCreateView.as_view(), name='crear_supervisor'),
    
]