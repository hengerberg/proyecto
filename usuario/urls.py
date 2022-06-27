from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', ProfileView.as_view(), name='perfil'),
    #usuarios
    path('user/list', UserListView.as_view(), name='lista_usuarios'),
    path('user/add', UserCreateView.as_view(), name='crear_usuario'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='editar_usuario'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='borrar_usuario'),
    # path('productos/<int:pk>', ProductInfoView.as_view(), name='info_producto'),
    # path('productos/edit/<int:pk>', ProductUpdateView.as_view(), name='actualizar_producto'),
    
    
]