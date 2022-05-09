from django.contrib import admin
from .models import Inventory, InventoryCurrent

# Register your models here.
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'chips_sale', 'chips_portability')
class InventoryCurrentAdmin(admin.ModelAdmin):
    list_display = ('user', 'chips_sale', 'chips_portability')


admin.site.register(Inventory,InventoryAdmin)
admin.site.register(InventoryCurrent,InventoryAdmin)