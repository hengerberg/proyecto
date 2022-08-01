from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, TemplateView,DeleteView
from django.urls.base import reverse_lazy
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from lider.mixins import ValidatePermissionRequiredMixin
from .form import IslaCreateForm
from .models import Isla, UserIsla
# Create your views here.


class IslaCreateView(ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'islas.add_isla'
    model = Isla
    form_class = IslaCreateForm
    template_name = 'isla/isla_add.html'
    success_url = reverse_lazy('isla:lista_islas')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form() # get_form() es lo mismo que escribir IslaCreateForm(request.POST)
                form.save(request.user.get_distributor_id(),commit=False)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Isla'
        context['titleForm'] = 'Nueva Isla'
        context['entity'] = 'Islas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['message'] = 'creado'
        return context


class IslaListView(ValidatePermissionRequiredMixin, ListView):
    permission_required = 'islas.view_isla'
    model = Isla
    template_name = 'isla/isla_list.html'

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
                for i in Isla.objects.filter(distributor_id=request.user.user_profile.distributor_id):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Islas'
        context['entity'] = 'Islas'
        context['create_url'] = reverse_lazy('isla:crear_isla')
        context['list_url'] = reverse_lazy('isla:lista_islas')
        return context


class IslaUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Isla
    form_class = IslaCreateForm
    template_name = 'isla/isla_update.html'
    success_url = reverse_lazy('isla:lista_islas')
    permission_required = 'lider.change_product'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
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
        context['title'] = 'Edición una Categoria'
        context['titleForm'] = 'Editar Isla'
        context['entity'] = 'Categorias'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['message'] = 'editado'
        return context


class IslaDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Isla
    template_name = 'isla/isla_delete.html'
    success_url = reverse_lazy('isla:lista_islas')
    permission_required = 'islas.delete_isla'
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
        context['title'] = 'Eliminacion de una Isla'
        context['entity'] = 'Islas'
        context['list_url'] = self.success_url
        context['action'] = 'del'
        return context


class IslaDetailView(ValidatePermissionRequiredMixin, TemplateView):
    
    template_name = 'isla/isla_detail.html'
    success_url = reverse_lazy('isla:lista_islas')
    permission_required = 'islas.delete_isla'
    url_redirect = success_url

    # def get(self, request, *args, **kwargs):
    #     sellers = UserIsla.objects.filter(isla = kwargs['pk'])
    #     print(sellers)
    #     context = {}
    #     return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de la Isla'
        context['entity'] = 'Islas'
        context['list_url'] = self.success_url
        context['action'] = 'del'
        context['sellers'] = UserIsla.objects.filter(isla = kwargs['pk'])
        return context
    

   