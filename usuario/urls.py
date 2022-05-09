from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('', inicio, name='inicio'),
    path('perfil/', ProfileView.as_view(), name='perfil'),
    path('accounts/', include('django.contrib.auth.urls')),
    
]