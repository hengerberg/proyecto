
from django.shortcuts import render
from django.views.generic import  TemplateView, ListView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls.base import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.db import transaction

from .mixins import IsLiderMixin
from inventory.models import Inventory, InventoryCurrent
from supervisor.forms import FormularioCrearVendedor
from usuario.models import Profile
from .models import Product
from .forms import FormAddProduct
# Create your views here.

"""
-----------permisos del lider------------------
1. ver informacion de todos los usuarios
2. ver informacion de los supervisores
3. modificar supervisores
4. agregar, actualizar, listar y eliminar productos
"""


class IndexView(IsLiderMixin,TemplateView):
    template_name = 'lider/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio'
        return context


class SupervisorCreateView(IsLiderMixin,CreateView):
    model = User
    form_class = FormularioCrearVendedor
    template_name = 'lider/supervisor_add.html'
    success_url = reverse_lazy('lider:inicio')

    # sobreescribimos el metodo post de la vista generica CreateView
    def post(self, request, *args, **kwargs):
        form = FormularioCrearVendedor(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # commit  = False es para decirle que no queremos guardar el modelo todavia
                supervisor = form.save(commit=False)
                # agrego datos que no estan definidos en el formulario
                supervisor.distribuidora = request.user.user_profile.distributor_id
                supervisor.cargo = 'supervisor'
                supervisor.save()
                # extraemos los datos del supervisor creado
                sup = User.objects.get(username=supervisor.username)
                #creamos el perfil
                perfil = Profile(distribuidora_id =request.user.user_profile.distributor_id, usuario_id = sup.id)
                perfil.save()
                #creamos el inventario
                inventory = Inventory(user_id=sup.id)
                inventory.save()
                inv = InventoryCurrent(user_id=sup.id)
                inv.save()
            return HttpResponseRedirect(self.success_url)
        # como no retorna nada colcamos self.object = None
        self.object = None
        # agregamos de nuevo el formulario con los errores devueltos
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de supervisor'
        context['titleForm'] = 'Supervisor'
        context['entity'] = 'Nuevo Spervisor'

        return context

    
class WorkersListView(IsLiderMixin, ListView):

    model = Profile
    template_name = 'lider/lista_trabajadores.html'

    # modificamos el queryset
    def get_queryset(self):
        return Profile.objects.filter(distribuidora_id=self.request.user.user_profile.distributor_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Vendedores'
        context['entity'] = 'Vendedores'
        return context



class ProductCreateView(IsLiderMixin, CreateView):
    model = Product
    form_class = FormAddProduct
    template_name = 'lider/crear_producto.html'
    success_url = reverse_lazy('lider:lista_productos')

    # sobreescribimos el metodo post de la vista generica CreateView
    def post(self, request, *args, **kwargs):
        form = FormAddProduct(request.POST)
        #print(request.user.user_profile.distribuidora_id)
        #print(form)
        if form.is_valid():
            print(form)
            
            return HttpResponseRedirect(self.success_url)
        # como no retorna nada colcamos self.object = None
        self.object = None
        # agregamos de nuevo el formulario con los errores devueltos
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de productos'
        context['entity'] = 'Nuevo Producto'
        return context




class ProductsListView(IsLiderMixin, ListView):
    model = Product
    template_name = 'lider/lista_productos.html'

    def get_queryset(self):
        return Product.objects.filter(distributor_id=self.request.user.user_profile.distributor_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Productos'
        context['entity'] = 'Productos'
        return context