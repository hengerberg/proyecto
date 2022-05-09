from django.contrib import admin
from .models import GrupSupervisor

class GrupSupervisorAdmin(admin.ModelAdmin):
    list_display =('supervisor','vendedor')
    

admin.site.register(GrupSupervisor, GrupSupervisorAdmin)