from django.shortcuts import render

# Create your views here.
def error404(request):

    return render(request, 'home/404.html')