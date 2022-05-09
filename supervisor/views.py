import json

from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.urls.base import reverse_lazy
from django.db import transaction
from django.contrib.auth.models import User

from .forms import FormularioCrearVendedor, SellerUpdateForm
from usuario.models import Profile
from .models import GrupSupervisor
from inventory.models import Inventory, InventoryCurrent
from inventory.functions import update_inventory, ordenes
from vendedor.models import Report, ReportDetail
from .mixins import IsSupervisorMixin


# Create your views here.

class IndexView(IsSupervisorMixin, TemplateView):
    template_name = 'supervisor/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio'
        
        return context


class SellerCreateView(IsSupervisorMixin, CreateView):
    model = User
    form_class = FormularioCrearVendedor
    template_name = 'supervisor/vendedor/crear_vendedor.html'
    success_url = reverse_lazy('supervisor:lista_vendedores')

    # sobreescribimos el metodo post de la vista generica CreateView
    def post(self, request, *args, **kwargs):
        form = FormularioCrearVendedor(request.POST)
        print(request.user.user_profile.distribuidora_id)
        if form.is_valid():
            # commit  = False es para decirle que no queremos guardar el modelo todavia
            vendedor = form.save()
            # agrego datos que no estan definidos en el formulario
        
            # extraemos los datos del vendedor creado
            ven = User.objects.get(username=vendedor.username)
            # agregamos al vendedor creado al su grupo correspondiente
            grupo = GrupSupervisor(supervisor_id=request.user.id, vendedor_id=ven.id)
            grupo.save()
            # agregamos al vendedor a su respectiva distribuidora
            distribuidora = Profile(usuario_id=ven.id, distribuidora_id=request.user.user_profile.distribuidora_id)
            distribuidora.save()
            inventory = Inventory(user_id=ven.id)
            inventory.save()
            inventory = InventoryCurrent(user_id=ven.id)
            inventory.save()
            return HttpResponseRedirect(self.success_url)
        # como no retorna nada colcamos self.object = None
        self.object = None
        # agregamos de nuevo el formulario con los errores devueltos
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de vendedores'
        context['entity'] = 'Nuevo Vendedor'
        return context


class SellerListView(IsSupervisorMixin, ListView):
    model = GrupSupervisor
    template_name = 'supervisor/vendedor/listar_vendedores.html'

    # modificamos el queryset
    def get_queryset(self):
        return GrupSupervisor.objects.filter(supervisor_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Vendedores'
        context['entity'] = 'Vendedores'
        return context


class SellerUpdateView(IsSupervisorMixin, UpdateView):
    model = User
    form_class = SellerUpdateForm
    template_name = "supervisor/vendedor/editar_vendedor.html"
    success_url = reverse_lazy('supervisor:lista_vendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Vendedor'
        context['entity'] = 'Editar Vendedor'
        return context


class SellerInfoInventoryListView(IsSupervisorMixin, ListView):
    
    model = Inventory
    template_name = 'supervisor/vendedor/informacion_vendedor.html'
    success_url = reverse_lazy('supervisor:lista_vendedores')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        
        query = InventoryCurrent.objects.get(user_id=self.kwargs['pk'])
        return query

    def post(self, request, *args, **kwargs):
        """
        por crear mensaje de error cuando el supervisor no tiene suficientes chip para agregar y 
        para retirar mas chips de los que tiene el vendedor
        """
        try:
            action = request.POST['action']
            if action == 'add':
                venta,portabilidad =request.POST.get('venta'),request.POST.get('portabilidad')
       
                if venta == '' and portabilidad == '':
                    return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])

                if venta == '': chip_venta = 0
                else: chip_venta = int(venta)
                
                if portabilidad == '': chip_portabilidad = 0
                else: chip_portabilidad = int(portabilidad)

                with transaction.atomic():
                    inv = InventoryCurrent.objects.get(user_id=request.user.id)
                    if inv.chips_sale >= chip_venta and inv.chips_portability >= chip_portabilidad:
                        #actualizo el inventario del vendedor
                        update_inventory(chip_venta, chip_portabilidad, self.kwargs['pk'], True)
                        # actualiza los datos del supervisor
                        update_inventory(-chip_venta, -chip_portabilidad, request.user.id, False)

                        return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])
                   
                return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])
            elif action == 'del':
                venta,portabilidad = request.POST.get('venta'),request.POST.get('portabilidad')
       
                if venta == '' and portabilidad == '':
                    return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])

                if venta == '': chip_venta = 0
                else: chip_venta = int(venta)
                
                if portabilidad == '': chip_portabilidad = 0
                else: chip_portabilidad = int(portabilidad)
                
                with transaction.atomic():
                    inv_ven = InventoryCurrent.objects.get(user_id=self.kwargs['pk'])
                    if inv_ven.chips_sale >= chip_venta and inv_ven.chips_portability >= chip_portabilidad:
                        #actualizo el inventario del vendedor
                        update_inventory(chip_venta* -1, chip_portabilidad* -1, self.kwargs['pk'], False)
                        #actualizo los datos del supervisor
                        update_inventory(chip_venta, chip_portabilidad, request.user.id, True)
                        return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])
                    
           
                return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])
            
            if action == 'searchdata':
                data = ordenes(request,self.kwargs['pk'])
            else:
                print('ha ocurrido un error')
        except Exception as e:
            print(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Inventario'
        context['entity'] = 'Agregar Inventario'
        return context


class InventoryUpdateView(IsSupervisorMixin, ListView):
    model = Inventory
    template_name = 'supervisor/agregar_inventario.html'
    #form_class = InventoryAddForm
    success_url = reverse_lazy('supervisor:agregar-inventario')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # modificamos el queryset
    def get_queryset(self):
        query1 = Inventory.objects.filter(user_id=self.request.user.id).last()
        query2 = InventoryCurrent.objects.filter(user_id=self.request.user.id).last()
        #en caso de que el vendedor aun no tenga datos en el inventario se crea por primera vez
        if query1 == None and query2 == None:
            x = Inventory(chips_sale = 0,chips_portability = 0,user_id = self.request.user.id)
            x.save()
            y = InventoryCurrent(chips_sale = 0,chips_portability = 0,user_id = self.request.user.id)
            y.save()
            return redirect(self.success_url)
        return query2

    def post(self, request, *args, **kwargs):
        
        try:
            action = request.POST['action']
            if action == 'add':
                if request.POST.get('venta') == '' and request.POST.get('portabilidad') == '':
                    return redirect(self.success_url)

                if request.POST.get('venta') == '': chip_venta = 0
                else: chip_venta = int(request.POST.get('venta'))

                if request.POST.get('portabilidad') == '': chip_portabilidad = 0
                else: chip_portabilidad = int(request.POST.get('portabilidad'))

                update_inventory(chip_venta, chip_portabilidad, self.request.user.id, True)

                return redirect(self.success_url)
            elif action == 'searchdata':
                data = []
                # filtramos los vendedores del supervisor logueado
                for v in GrupSupervisor.objects.filter(supervisor_id=request.user.id):
                    # vamos agregando los reportes de cada vendedor en data[]
                    for i in Inventory.objects.filter(user_id=v.vendedor_id):
                        data.append(i.toJSON())
                        #data.insert(0,i.toJSON())
                data.sort(key=lambda x: x['id'], reverse=True)
                print(data)
            else:
                print('ha ocurrido un error')
        except Exception as e:
            print(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Editar Vendedor'
        context['entity'] = 'Editar Vendedor'
        return context
    

class LiquidationsListView(IsSupervisorMixin, ListView):
    model = GrupSupervisor
    template_name = 'supervisor/liquidaciones.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # filtramos los vendedores del supervisor logueado
                for v in GrupSupervisor.objects.filter(supervisor_id=request.user.id):
                    # vamos agregando los reportes de cada vendedor en data[]
                    for i in Report.objects.filter(user_id=v.vendedor_id):
                        data.insert(0,i.toJSON())
                
            elif action == 'search_details_prod':
                data = []
                for i in ReportDetail.objects.filter(report_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'cancel_liquidations':
                liq = Report.objects.get(id=request.POST['id'])
                liq.state = 'cancelado'
                liq.save()
            elif action == 'aprobado_liquidations':
                # guardamos todos los datos en vents
                vents = json.loads(request.POST['vents'])
                ventas = 0
                portas = 0
                for i in vents['det']:
                    if i['product']['category'] == 1:
                        ventas += 1 * i['quantity']
                    else:
                        portas += 1 * i['quantity']
                with transaction.atomic():  # en caso de que haya un error en la insercion no guardamos nada
                    liq = Report.objects.get(id=vents['id'])
                    liq.state = 'aprobado'
                    liq.save()
                    update_inventory(ventas*-1,portas*-1,vents['user_id'], False)
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
                data['error'] = str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Liquidaciones'
        context['entity'] = 'Liquidaciones'
        return context

