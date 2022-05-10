from pipes import Template
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'lider'
urlpatterns = [
    path('', IndexView.as_view(), name='inicio'),
    path('supervisor/add', SupervisorCreateView.as_view(), name='crear_supervisor'),
    path('supervisor/trabajadores', WorkersListView.as_view(), name='lista_trabajadores'),
    #productos
    path('productos/list', ProductsListView.as_view(), name='lista_productos'),
    path('productos/add', ProductCreateView.as_view(), name='agregar_producto'),
    
]