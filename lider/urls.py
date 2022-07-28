from pipes import Template
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'lider'
urlpatterns = [
   
    path('supervisor/add', SupervisorCreateView.as_view(), name='crear_supervisor'),
    #productos
    path('productos/list', ProductsListView.as_view(), name='lista_productos'),
    path('productos/add', ProductCreateView.as_view(), name='agregar_producto'),
    path('productos/<int:pk>', ProductInfoView.as_view(), name='info_producto'),
    path('productos/edit/<int:pk>', ProductUpdateView.as_view(), name='actualizar_producto'),
    path('add/cat/produc/<int:pk>', CatProductCreateView.as_view(), name='automatic'),
    
]