import json
import re

from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.urls.base import reverse_lazy
from django.db import transaction
from usuario.models import User
from django.contrib import messages
from .forms import SalesCreateForm, SellerUpdateForm,SellerCreateForm
from usuario.models import Profile
from .models import GrupSupervisor
from inventory.models import Inventory, InventoryCurrent
from inventory.functions import update_inventory, ordenes
from vendedor.models import Report, ReportDetail
from lider.mixins import ValidatePermissionRequiredMixin


# Create your views here.

'''
permisos de supervisor
usuario.add_seller
usuario.view_seller
usuario.change_seller
usuario.del_seller
inventory.view_inventory
inventory.change_inventory
vendedor.view_report

por terminar reparar la vista SellerInfoInventoryListView
'''

class SellerCreateView(ValidatePermissionRequiredMixin,CreateView):
    permission_required = 'usuario.add_seller'
    model = User
    form_class = SellerCreateForm
    template_name = 'supervisor/vendedor/crear_vendedor.html'
    success_url = reverse_lazy('supervisor:lista_vendedores')

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
                    # agregamos al vendedor al grupo de vendedores
                    sup_group = GrupSupervisor(supervisor_id=request.user.id, vendedor_id = user.id)
                    sup_group.save()
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
        context['title'] = 'Registro de vendedores'
        context['entity'] = 'Nuevo Vendedor'
        context['titleForm'] = 'Nuevo Usuario'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class SellerListView(ValidatePermissionRequiredMixin,ListView):
    permission_required = 'usuario.view_seller'
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


class SellerUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    permission_required = 'usuario.change_seller'
    model = User
    form_class = SellerUpdateForm
    template_name = "supervisor/vendedor/editar_vendedor.html"
    success_url = reverse_lazy('supervisor:lista_vendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Vendedor'
        context['entity'] = 'Editar Vendedor'
        return context


class SellerInfoInventoryListView(ValidatePermissionRequiredMixin,UpdateView):
    permission_required = 'usuario.view_seller'
    model = Inventory
    form_class = SellerUpdateForm
    template_name = 'supervisor/vendedor/informacion_vendedor.html'
    success_url = reverse_lazy('supervisor:lista_vendedores')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
       
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                venta,porta = request.POST['venta'],request.POST['portabilidad']
                if venta == '': venta = 0
                else: venta = int(venta)
                if porta == '': porta = 0
                else: porta = int(porta)
                if venta > 0 or porta > 0:
                    with transaction.atomic():
                        inv = InventoryCurrent.objects.get(user_id=request.user.id)
                        if inv.chips_sale >= venta and inv.chips_portability >= porta:
                            #actualizo el inventario del vendedor
                            update_inventory(venta, porta, self.kwargs['pk'], True)
                            # actualiza los datos del supervisor
                            update_inventory(-venta, -porta, request.user.id, False)

                            return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])
                messages.error(self.request, 'No tienes suficientes chips')
                return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])
            elif action == 'del':
                venta,porta = request.POST['venta'],request.POST['portabilidad']
                if venta == '': venta = 0
                else: venta = int(venta)
                if porta == '': porta = 0
                else: porta = int(porta)
       
                if venta > 0 or porta > 0:
                    with transaction.atomic():
                        inv_ven = InventoryCurrent.objects.get(user_id=self.kwargs['pk'])
                        if inv_ven.chips_sale >= venta and inv_ven.chips_portability >= porta:
                            #actualizo el inventario del vendedor
                            update_inventory(venta* -1, porta* -1, self.kwargs['pk'], False)
                            #actualizo los datos del supervisor
                            update_inventory(venta, porta, request.user.id, True)
                            return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])
                messages.error(self.request, 'El vendedor no tiene suficientes chips')
                return redirect('supervisor:informacion_vendedor', pk=self.kwargs['pk'])
            elif action == 'searchdata':
                data = ordenes(request,self.kwargs['pk'])
            else:
                messages.info(self.request, 'Ha ocurrido un error')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Inventario'
        context['entity'] = 'Agregar Inventario'
        context['object_list'] = InventoryCurrent.objects.get(user_id=self.kwargs['pk'])
        return context


class InventoryUpdateView(ValidatePermissionRequiredMixin,ListView):
    permission_required = 'inventory.change_inventory'
    model = Inventory
    template_name = 'supervisor/agregar_inventario.html'
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
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                venta,porta = request.POST['venta'],request.POST['portabilidad']
                if venta == '': venta = 0
                else: venta = int(venta)
                if porta == '': porta = 0
                else: porta = int(porta)
                # comprobamos que los campos no sean ceros
                if venta > 0 or porta > 0:
                    #actualizamos el inventario
                    update_inventory(venta, porta, self.request.user.id, True)
                return redirect(self.success_url)
            elif action == 'searchdata':
                data = []
                # filtramos los vendedores del supervisor logueado
                for v in GrupSupervisor.objects.filter(supervisor_id=request.user.id):
                    # vamos agregando los reportes de cada vendedor en data[]
                    for i in Inventory.objects.filter(user_id=v.vendedor_id):
                        #data.append(i.toJSON())
                        data.insert(0,i.toJSON())
                data.sort(key=lambda x: x['id'], reverse=True)
                
            else:
                data['error'] = 'ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        print(data)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi Inventario'
        context['entity'] = 'Inventario'
        return context
    

class LiquidationsListView(ValidatePermissionRequiredMixin,ListView):
    permission_required = ['vendedor.view_report','vendedor.delete_report','vendedor.view_reportdetail']
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
                    if i['product']['cat']['name'] == 'ventas':
                        ventas += 1 * i['quantity']
                    if i['product']['cat']['name'] == 'portabilidad':
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



class SalesCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permission_required = 'vendedor.view_inventory'
    # Or multiple permissions
    #permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!
    model = Report
    permission_required = 'supervisor.add_grupsupervisor'
    form_class = SalesCreateForm
    template_name = 'supervisor/liquidar-ventas.html'
    success_url = reverse_lazy('supervisor:liquidaciones')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                for v in GrupSupervisor.objects.filter(supervisor_id=request.user.id):
                    # vamos agregando los reportes de cada vendedor en data[]
                    for i in Report.objects.filter(user_id=v.vendedor_id, state = 'aprobado'):
                        data.insert(0,i.toJSON())  
            elif action == 'search_details_prod':
                data = []
                for i in ReportDetail.objects.filter(report_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'add':  # recibimos el valor del input oculto con el valor que le enviamos en el contexto
                # guardamos en vents los productos que nos llega del formulario
                vents = json.loads(request.POST['vents'])
                #print(vents['products'])
                with transaction.atomic():  # en caso de que haya un error en la insercion no guardamos nada
                    report = Report()
                    report.user_id = self.request.user.id
                    report.state = 'finalizado'
                    report.date = vents['date']
                    report.subtotal = float(vents['subtotal'])
                    report.commission_paid = float(vents['commission_paid'])
                    report.commission_receivable = float(vents['commission_receivable'])
                    report.discount = float(vents['discount'])
                    report.total = float(vents['total'])
                    report.save()  # guardamos los datos del reporte

                    # vamos guardando los datos de los productos del reporte
                    for i in vents['products']:
                        # vamos agregando el detalle del reporte
                        for j in i['det']:
                            det = ReportDetail()
                            det.report_id = report.id
                            det.product_id = j['product']['id']
                            det.quantity = int(j['quantity'])
                            det.price = float(j['price'])
                            det.commission_paid = float(j['commission_paid'])
                            det.commission_receivable = float(j['commission_receivable'])
                            det.total = float(j['total'])
                            det.save()

                        Report.objects.filter(id=i['id']).update(state='finalizado') # actualizo el reporte a finalizado
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        # para que se pueda serializar se coloca safe = false
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Liquidacion de Ventas'
        context['entity'] = 'Nueva Liquidacion'
        context['action'] = 'add'
        return context


class SalesListView(ValidatePermissionRequiredMixin,ListView):
    permission_required = 'supervisor.add_grupsupervisor'
    model = Report
    template_name = 'supervisor/lista-ventas.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Report.objects.filter(user_id=self.request.user.id):
                    data.insert(0,i.toJSON())
                    #data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in ReportDetail.objects.filter(report_id=request.POST['id']):
                    data.insert(0,i.toJSON())
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

