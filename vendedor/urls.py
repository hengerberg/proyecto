from django.urls import path

from .views import *

app_name = 'vendedor'
urlpatterns = [
    
    #reportes
    path('reporte/add', ReportCreateView.as_view(), name='crear-reporte'),
    path('reporte/list', ReportListView.as_view(), name='lista-reportes'),
    path('ventas', MySalesListView.as_view(), name='ventas'),
    path('inventario', InventoryListView.as_view(), name='inventario'),
    
    
]