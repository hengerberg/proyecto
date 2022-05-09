from django.shortcuts import render
from django.views.generic import  TemplateView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls.base import reverse_lazy
from django.http.response import HttpResponseRedirect

from .mixins import IsLiderMixin
from inventory.models import Inventory
from supervisor.forms import FormularioCrearVendedor
# Create your views here.

    
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
            # commit  = False es para decirle que no queremos guardar el modelo todavia
            supervisor = form.save(commit=False)
            # agrego datos que no estan definidos en el formulario
            supervisor.distribuidora = request.user.distribuidora
            supervisor.cargo = 'supervisor'
            supervisor.save()
            # extraemos los datos del supervisor creado
            sup = User.objects.get(username=supervisor.username)
            inventory = Inventory(user_id=sup.id)
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
        context['title'] = 'Registro de supervisor'
        context['titleForm'] = 'Supervisor'
        context['entity'] = 'Nuevo Spervisor'

        return context

    