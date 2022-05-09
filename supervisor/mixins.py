from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib import messages

#clase para validar que el usuario este logeado y tenga el cargo correspondiente
class IsSupervisorMixin(object):
    @method_decorator(login_required)  
    def dispatch(self, request, *args, **kwargs):
        #print(request.user.get_all_permissions())
        permisos = ['supervisor.view_grupsupervisor'] # coloco los permisos necesarios para acceder
        if request.user.has_perms(permisos) : # preguntamos si el usuario tiene los permisos requeridos
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para ingresar a este modulo')
        return redirect('inicio')