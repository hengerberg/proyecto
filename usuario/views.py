import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout,update_session_auth_hash
from django.views.generic import UpdateView
from django.urls.base import reverse_lazy
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import RedirectView, ListView, CreateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
import Appgestion.settings as setting
from Appgestion import settings

from .forms import ProfileForm, UserForm, ProfileUpdateForm, ResetPasswordForm,ChangePasswordForm
from .models import Profile, User
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


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'usuario/perfil.html'
    success_url = reverse_lazy('user:perfil')

    def get_object(self):
        #consultamos si el perfil existe, si no existe lo crea
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return Profile.objects.create(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil'
        context['entity'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'usuario/editar_perfil.html'
    success_url = reverse_lazy('user:perfil')

    def dispatch(self, request, *args, **kwargs):
        # como es un update hay que darle valor al objeto object
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    # como no le pasamos el id por la url debemos instanciar el usuario que esta logueado y asi
    # poder darle valor al objeto object en el dispatch
    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
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
        context['title'] = 'Edicion de Perfil'
        context['titleForm'] = 'Editar Perfil'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserChagePasswordView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'registration/cambiar_password.html'
    success_url = reverse_lazy('user:login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #sobreescribimos el metodo get_form que es el que contiene el inicializador del formulario
    def get_form(self, form_class=None):
        #con esto inicializamos el formulario con el usuario actual
        form = PasswordChangeForm(user=self.request.user)
        # le cambiamos los atributos al formulario base
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['old_password'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su nueva contraseña'
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'
        return form


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user) # esta funcion permite No cerrar sesion al cambiar la contraseña
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'no ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de Contraseña'
        context['titleForm'] = 'Editar Contraseña'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = 'registration/resetpwd.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # creamos un metodo para enviar el correo electronico
    # enviamos todo el usuario como parametro
    def send_email_reset_pwd(self, user):
        data = {}
        try:
            # estamos trabajando en produccion enviamos el dominio de lo contrario enviamos 127.0.0.1:8000 (self.request.META['HTTP_HOST'])
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4() # generamos el token
            user.save() # guardamos el token

            #conectar con el servidor
            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            print('conectado..')

            email_to = user.email
            
            mensaje = MIMEMultipart()
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Reseteo de contraseña'

            content = render_to_string('registration/send_email.html', {
                'user': user,
                'link_resetpwd': 'http://{}/change/password/{}/'.format(URL, str(user.token)), # armamos la url
                'link_home': 'http://{}'.format(URL)
                })

            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ResetPasswordForm(request.POST)  # self.get_form()
            if form.is_valid():
                user = form.get_user() # obtenemos el usuario actual
                data = self.send_email_reset_pwd(user) # enviamos el correo 
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_sistem'] = 'nombre del sistema'
        context['title'] = 'Reseteo de Contraseña'
        return context


class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = 'registration/changepwd.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el metodo get para validar la url
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token'] # recogemos el valor del token que nos llega por la url
        # si existe ese token le damos paso al formulario de reseteo de contraseña si no lo enviamos a la raiz
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4() # generamos un nuevo token para que el usuario no pueda ingresar otra vez con la url antigua
                user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_sistem'] = 'nombre del sistema'
        context['title'] = 'Reseteo de Contraseña'
        context['login_url'] = settings.LOGIN_URL
        return context

# CRUD de usuarios
class UserListView(ValidatePermissionRequiredMixin, ListView):
    """
    vista que muestra todos los usuarios registrados en una distribuidora
    """
    permission_required = ('usuario.view_user','usuario.view_seller', 'usuario.view_supervisor')
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
                for i in User.objects.filter(user_profile__distributor_id=self.request.user.user_profile.distributor_id):
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
    template_name = 'usuario/crear_usuario.html'
    success_url = reverse_lazy('user:lista_usuarios')
    permission_required = 'usuario.add_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    form = self.get_form()
                    data = form.save()
                    # extraemos los datos del usuario creado
                    user = User.objects.get(username=data['username'])
                    #creamos el perfil
                    perfil = Profile(distributor_id=request.user.user_profile.distributor_id, user_id=user.id)
                    perfil.save()
                    if user.groups.filter(name__in=['supervisor', 'vendedor']): # comprobamos si el usuario tiene asignado alguno de estos grupos
                        #creamos el inventario
                        inventory = Inventory(user_id=user.id)
                        inventory.save()
                        inv = InventoryCurrent(user_id=user.id)
                        inv.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['titleForm'] = 'Nuevo Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class UserUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'usuario/editar_usuario.html'
    success_url = reverse_lazy('user:lista_usuarios')
    permission_required = 'usuario.change_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        # como es un update hay que darle valor al objeto object
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
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
        context['titleForm'] = 'Editar Usuario'
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
        # como es un update hay que darle valor al objeto object
        self.object = self.get_object()
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
