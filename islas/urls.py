from pipes import Template
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'isla'
urlpatterns = [
   
    path('add/', IslaCreateView.as_view(), name='crear_isla'),
    path('list/', IslaListView.as_view(), name='lista_islas'),
    path('delete/<int:pk>/', IslaDeleteView.as_view(), name='borrar_isla'),
    path('update/<int:pk>/', IslaUpdateView.as_view(), name='actualizar_isla'),
    path('detalle-isla/<int:pk>/', IslaDetailView.as_view(), name='detalle_isla'),

    
    
]