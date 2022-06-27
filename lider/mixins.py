from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.contrib import messages


#mixin personalizado para validar los permisos en las vistas
class ValidatePermissionRequiredMixin(object):
    permission_required = '' # permisos requeridos
    url_redirect = None # url para redireccionar en caso de no tener el permiso

    # validamos los permisos requeridos
    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms
    
    #validamos la url_redirec
    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('home:dashboard') # cambiar a login luego que se creen la validaciones del usuario si esta o no autenticado
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para ingresar a este modulo') # modulo de django para el envio de mensajes
        return redirect(self.get_url_redirect())