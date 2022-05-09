from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


#clase para validar que el usuario este logeado y tenga el cargo correspondiente
"""class RedirectMixin(object):
    @method_decorator(login_required)  
    def dispatch(self, request, *args, **kwargs):
        if request.user.cargo == 'supervisor':
           return redirect('supervisor:inicio')
        elif request.user.cargo == 'vendedor':
            return redirect('vendedor:inicio')
        else:
            return redirect('vendedor:otros')"""
            
        