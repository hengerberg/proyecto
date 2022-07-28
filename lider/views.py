
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls.base import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.db import transaction

from .mixins import ValidatePermissionRequiredMixin
from inventory.models import Inventory, InventoryCurrent
from supervisor.forms import FormularioCrearVendedor
from usuario.models import Profile
from .models import Product, Category
from .forms import FormAddProduct
# Create your views here.


"""
-----------permisos del lider------------------
usuario.view_seller
usuario.add_seller
usuario.view_supervisor'
usuario.view_user'
usuario.add_supervisor
lider.add_product
lider.change_product
lider.del_product
lider.view_product

"""


class SupervisorCreateView(ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'usuario.add_supervisor'
    model = User
    form_class = FormularioCrearVendedor
    template_name = 'lider/supervisor_add.html'
    success_url = reverse_lazy('lider:lista_trabajadores')

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
                perfil = Profile(
                    distributor_id=request.user.user_profile.distributor_id, user_id=sup.id)
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


# vistas de los productos

class ProductCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Product
    # enviamos los permisos necesarios para acceder a esta vista
    permission_required = 'lider.add_product'
    form_class = FormAddProduct
    template_name = 'lider/productos/crear_producto.html'
    success_url = reverse_lazy('lider:lista_productos')

    # sobreescribimos el metodo post de la vista generica CreateView
    def post(self, request, *args, **kwargs):
        form = FormAddProduct(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.distributor_id = request.user.user_profile.distributor_id
            product.save()

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


class ProductInfoView(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'lider.view_product'
    template_name = 'lider/productos/info_producto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informacion del Producto'
        context['entity'] = 'Productos'
        context['product'] = Product.objects.get(id=kwargs['pk'])
        return context


class ProductUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'lider.change_product'
    model = Product
    form_class = FormAddProduct
    template_name = 'lider/productos/actualizar_producto.html'
    success_url = reverse_lazy('lider:lista_productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Producto'
        context['entity'] = 'Editar Producto'
        return context


class ProductsListView(ValidatePermissionRequiredMixin, ListView):
    permission_required = 'lider.view_product'
    model = Product
    template_name = 'lider/productos/lista_productos.html'

    def get_queryset(self):
        return Product.objects.filter(distributor_id=self.request.user.user_profile.distributor_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Productos'
        context['entity'] = 'Productos'
        return context


class CatProductCreateView(ValidatePermissionRequiredMixin, TemplateView):
    
    permission_required = 'lider.add_product'
    template_name = 'lider/inicio.html'
    success_url = reverse_lazy('lider:lista_productos')

    # sobreescribimos el metodo post de la vista generica CreateView
    def get(self, request, *args, **kwargs):
        dist = self.request.user.user_profile.distributor_id
        cats = {
                '1':'ventas',
                '2':'portabilidad'
            }
        
        prods = {
                '1':{
                    'category': 'portabilidad',
                    'name': 'portabilidad',
                    'description': 'Portabilidad',
                    'price_in':0,
                    'price_out':0,
                    'seller_commission': 1.5
                },
                '2':{
                    'category': 'portabilidad',
                    'name': 'reposicion',
                    'description': 'reposicion',
                    'price_in':2.5,
                    'price_out':4,
                    'seller_commission': 1.5
                },
                '3':{
                    'category': 'ventas',
                    'name': 'chip $4',
                    'description': 'chip $4',
                    'price_in':2.5,
                    'price_out':4,
                    'seller_commission': 1.5
                },
                '4':{
                    'category': 'ventas',
                    'name': 'chip $7',
                    'description': 'chip $7',
                    'price_in':5.5,
                    'price_out':7,
                    'seller_commission': 1.5
                },
                '5':{
                    'category': 'ventas',
                    'name': 'chip $10',
                    'description': 'Portabilidad',
                    'price_in':8.5,
                    'price_out':10,
                    'seller_commission': 1.5
                },
                '6':{
                    'category': 'ventas',
                    'name': 'chip $20',
                    'description': 'Portabilidad',
                    'price_in':18.5,
                    'price_out':20,
                    'seller_commission': 1.5
                },
                '7':{
                    'category': 'ventas',
                    'name': 'chip $25',
                    'description': 'Portabilidad',
                    'price_in':23.5,
                    'price_out':25,
                    'seller_commission': 1.5
                }
            }
        if Category.objects.all() != '' and kwargs['pk'] == 1:
            try:
                # creamos las categorias
                for cat in cats.values():
                    c = Category(name = cat, distributor_id = dist)
                    c.save()

                # creamos los productos
                for proct in prods.values():
                    c = Category.objects.get(name = proct['category'])
                    p = Product(
                        name = proct['name'],
                        description = proct['description'],
                        price_in = proct['price_in'],
                        price_out = proct['price_out'],
                        seller_commission = proct['seller_commission'],
                        pay_commission = True,
                        category_id = c.id,
                        distributor_id = dist
                    )
                    p.save()
            except Exception as e:
                print(e)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de productos'
        context['entity'] = 'Nuevo Producto'

        return context