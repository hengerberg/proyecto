from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def error404(request):

    return render(request, 'home/404.html')

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'home/dashboard.html'
