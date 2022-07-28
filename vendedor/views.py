import json
import datetime

from django.db import transaction
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q

from inventory.models import Inventory, InventoryCurrent
from inventory.functions import ordenes
from .models import Product, Report, ReportDetail
from lider.mixins import ValidatePermissionRequiredMixin
from .forms import ReportForm

# Create your views here.

# LoginRequiredMixin es el mixin que trae django incorporado, tambien se puede usar
# el decorador @login_required

"""
permisos
report.add_report
vendedor.view_report
vendedor.view_reportdetail
inventory.view_inventory
"""

class ReportCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    #permission_required = 'vendedor.view_inventory'
    # Or multiple permissions
    #permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!
    model = Report
    permission_required = 'vendedor.add_report'
    form_class = ReportForm
    template_name = 'vendedor/reportar-ventas.html'
    success_url = reverse_lazy('vendedor:lista-reportes')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids']) # convertimos a lista los id de los productos que vamos a excluir
                prods = Product.objects.filter(
                    name__icontains=request.POST['term'],
                    is_active=True)
                for i in prods.exclude(id__in = ids_exclude):
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'add':  # recibimos el valor del input oculto con el valor que le enviamos en el contexto
                # guardamos en vents lo que nos llega del formulario
                vents = json.loads(request.POST['vents'])
                #print(vents['products'])
                ventas = {'ventas':0, 'portabilidades':0} # las categorias de los productos
                for item in vents['products']:
                    if item['cat']['name'] == 'ventas': 
                        ventas['ventas'] += int(item['cant'])
                    if item['cat']['name'] == 'portabilidades': 
                        ventas['portabilidades'] += int(item['cant'])

                inventario = InventoryCurrent.objects.get(user_id = self.request.user.id)
                # comprobamos que el vendedor tenga los suficientes chips en el inventario
                if inventario.chips_sale >= ventas['ventas'] and inventario.chips_portability >= ventas['portabilidades']:

                    with transaction.atomic():  # en caso de que haya un error en la insercion no guardamos nada

                        report = Report()
                        report.user_id = self.request.user.id
                        report.date = vents['date']
                        report.subtotal = float(vents['subtotal'])
                        report.commission_paid = float(vents['commission_paid'])
                        report.commission_receivable = float(vents['commission_receivable'])
                        report.discount = float(vents['discount'])
                        report.total = float(vents['total'])
                        report.save()  # guardamos los datos del reporte

                        # vamos guardando los datos de los productos del reporte
                        for i in vents['products']:
                            det = ReportDetail()
                            det.report_id = report.id
                            det.product_id = i['id']
                            det.quantity = int(i['cant'])
                            det.price = float(i['price_in'])
                            det.commission_paid = float(i['commission_paid'])
                            det.commission_receivable = float(i['commission_receivable'])
                            det.total = float(i['subtotal'])
                            det.save()
                else:
                    data['error'] = 'No tienes suficiente inventario'
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


class ReportListView(ValidatePermissionRequiredMixin,ListView):
    permission_required = 'vendedor.view_report'
    model = Report
    template_name = 'vendedor/lista-reportes.html'

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


class MySalesListView(ValidatePermissionRequiredMixin,ListView):
    permission_required = 'vendedor.view_reportdetail'
    template_name = 'vendedor/mis-ventas.html'

    def get_queryset(self):

        day = datetime.datetime.today().day
        self.month = datetime.datetime.today().month
        year = datetime.datetime.today().year
        start_date = datetime.date(year, self.month, 1)
        end_date = datetime.date(year, self.month, day)
        # utilizamos el objeto Q para combinar dos o mas consultas
        liquidaciones = ReportDetail.objects.filter(Q(report__user_id = self.request.user.id,
                                                    report__state = 'finalizado',
                                                    report__date__range=(start_date, end_date)) | Q(report__user_id = self.request.user.id,
                                                    report__state = 'aprobado',
                                                    report__date__range=(start_date, end_date)))
        products = Product.objects.all()
        self.products= {} #aqui vamos a guardar los datos relacionados con los productos vendidos
        
        for product in products:
            #filtro todos los productos, se suman las cantidades y se agraga solo el total al dict productos
            self.products[product.name] = liquidaciones.filter(product_id = product.id).aggregate(
                Sum('quantity'),
                comision_pagada=Sum('commission_paid'),
                comision_por_cobrar=Sum('commission_receivable'),
                total=Sum('commission_paid')+Sum('commission_receivable')
                )
            
        for product in self.products:
            for key in self.products[product]:
                if self.products[product][key] == None:
                    self.products[product][key] = 0
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mis Ventas'
        context['entity'] = 'Ventas'
        context['month'] = datetime.datetime.today()
        context['products'] = self.products # se agrega el dict products al context
       
        return context


class InventoryListView(ListView):
    permission_required = 'inventory.view_inventory'
    model = Inventory
    template_name = 'vendedor/inventario.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = ordenes(request, self.request.user.id)
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            data = InventoryCurrent.objects.get(user_id=self.request.user.id)
        except Exception as e:
            data = messages.error(self.request, 'No tienes inventario asociado')

        context['inventario_actual'] = data
        context['title'] = 'Inventario'
        context['entity'] = 'Inventario'
        return context