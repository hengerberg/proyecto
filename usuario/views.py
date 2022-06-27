from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views.generic import  UpdateView
from django.urls.base import reverse_lazy
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import RedirectView,ListView,CreateView,DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from .forms import ProfileForm,UserForm,UserFormB
from .models import  Profile, User
from lider.mixins import ValidatePermissionRequiredMixin
import Appgestion.settings as setting
from inventory.models import Inventory, InventoryCurrent

"""
permisos
'usuario.view_user'
'usuario.view_seller'
'usuario.view_supervisor'
'usuario.add_user'
'usuario.change_user'
'usuario.delete_user'

"""

class LoginFormView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        context['name_sistem'] = 'Nombre del sistema'
        return context

class LogoutView(RedirectView):
    pattern_name = 'user:login'
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class ProfileView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'usuario/perfil.html'
    success_url = reverse_lazy('perfil')

    def get_object(self):
        #consultamos si el perfil existe, si no existe lo crea
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return Profile.objects.create(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil'
        return context

# CRUD de usuarios 
class UserListView(ValidatePermissionRequiredMixin,ListView):
    """
    vista que muestra todos los usuarios registrados en una distribuidora
    """
    permission_required = ('usuario.view_user','usuario.view_seller','usuario.view_supervisor')
    model = User
    template_name = 'usuario/lista_usuarios.html'

    # el metodo dispatch sirve para direccionar el tipo de peticion se por POST o GET
    # lo utilizamos cuando sobreescribimos el metodo del tipo de peticion
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in User.objects.filter(user_profile__distributor_id = self.request.user.user_profile.distributor_id):
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de trabajadores'
        context['entity'] = 'Trabajadores'
        context['create_url'] = reverse_lazy('user:crear_usuario')
        context['list_url'] = reverse_lazy('user:lista_usuarios')
        return context

class UserCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'usuario/crear_usuario2.html'
    success_url = reverse_lazy('user:lista_usuarios')
    permission_required = 'usuario.add_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        user = UserFormB(request.POST)
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    form = self.get_form()
                    data = form.save()
                    # extraemos los datos del usuario creado
                    sup = User.objects.get(username=data['username'])
                    #creamos el perfil
                    perfil = Profile(distributor_id=request.user.user_profile.distributor_id, user_id=sup.id)
                    perfil.save()
                    #creamos el inventario
                    inventory = Inventory(user_id=sup.id)
                    inventory.save()
                    inv = InventoryCurrent(user_id=sup.id)
                    inv.save()
            
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['titleForm'] = 'Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class UserUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'usuario/crear_usuario2.html'
    success_url = reverse_lazy('user:lista_usuarios')
    permission_required = 'usuario.change_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object() # como es un update hay que darle valor al objeto object
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        user = UserFormB(request.POST)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de un Usuario'
        context['titleForm'] = 'Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class UserDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'usuario/borrar_usuario.html'
    success_url = reverse_lazy('user:lista_usuarios')
    permission_required = 'usuario.delete_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object() # como es un update hay que darle valor al objeto object
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'del'
        return context