from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect
from django.views.generic import  UpdateView
from django.urls.base import reverse_lazy
from Appgestion import settings

from .forms import ProfileForm
from .models import  Profile

# @login_required


def inicio(request):
    """
        vista basada en funcion que permite a los usuarios ser 
        redireccionados segun sus permisos
    """

    if request.user.is_authenticated:
        
        #para verificar que permiso tiene el usuario al iniciar session
        print(request.user.get_all_permissions())

        if request.user.has_perms(['supervisor.view_grupsupervisor']):
            return redirect('supervisor:inicio')
            
        elif request.user.has_perms(['vendedor.add_report']):
            return redirect('vendedor:inicio')
        elif request.user.has_perms(['inventory.add_inventory']):
            return redirect('lider:inicio')
        else: return redirect('vendedor:otros')
        
    else:
        return HttpResponseRedirect('/accounts/login')


class ProfileView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'perfil.html'
    success_url = reverse_lazy('perfil')

    def get_object(self):
        #consultamos si el perfil existe, si no existe lo crea
        try:
            return Profile.objects.get(usuario=self.request.user)
        except Profile.DoesNotExist:
            return Profile.objects.create(usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil'
        return context
    
        

    #user = Usuario.objects.get(profile__id=request.user.id)
    #print(user)
    #return render(request, 'perfil.html', {'form': form})