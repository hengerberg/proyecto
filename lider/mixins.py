from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from django.contrib import messages


#clase para validar que el usuario este logeado y tenga los permisos correspondiente
class IsLiderMixin(object):
    @method_decorator(login_required)  
    def dispatch(self, request, *args, **kwargs):
        permisos = ['inventory.add_inventory'] # coloco los permisos necesarios para acceder

        if request.user.has_perms(permisos) : # preguntamos si el usuario tiene los permisos requeridos
            return super().dispatch(request, *args, **kwargs)
    
        messages.error(request, 'No tienes permisos para ingresar a este modulo')
        return redirect('inicio')