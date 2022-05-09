from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'supervisor'
urlpatterns = [
    path('', IndexView.as_view(), name='inicio'),
    #vendedor
    path('vendedor/add', SellerCreateView.as_view(), name='crear_vendedor'),
    path('vendedor/list', SellerListView.as_view(), name='lista_vendedores'),
    path('vendedor/edit/<int:pk>', SellerUpdateView.as_view(), name='editar_vendedor'),
    path('vendedor/<int:pk>', InfoSellerListView.as_view(), name='informacion_vendedor'),
    
    

    path('inventario/add', InventoryUpdateView.as_view(), name='agregar-inventario'),

    path('liquidaciones/', LiquidationsListView.as_view(), name='liquidaciones')

    
]