from django.contrib import admin
from .models import Isla, UserIsla, SalesIsla



class IslaAdmin(admin.ModelAdmin):
    list_display = ('name','address','description')

class UserIslaAdmin(admin.ModelAdmin):
    list_display = ('isla', 'user')

class SaleIslaAdmin(admin.ModelAdmin):
    list_display = ('isla','user','name','ci','min','icc','chip','nip','operadora','nota')
    


admin.site.register(Isla, IslaAdmin)
admin.site.register(UserIsla, UserIslaAdmin)
admin.site.register(SalesIsla, SaleIslaAdmin)
