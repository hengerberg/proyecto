from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict

from usuario.models import User

# Create your models here.
class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chips_sale = models.IntegerField(default=0)
    chips_portability = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    type = models.BooleanField(default=True) # True=Add, False=Del
    
    class Meta:
        db_table = 'inventory'

    def toJSON(self):
        item = model_to_dict(self) # permite devolver todos los parametros del modelo en un diccionario
        item['user'] = self.user.first_name + ' ' + self.user.last_name
        item['date'] = self.created.strftime('%Y-%m-%d')
        item['chips_sale'] = format(self.chips_sale)
        item['chips_portability'] = format(self.chips_portability)
        
        return item



class InventoryCurrent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chips_sale = models.IntegerField(default=0)
    chips_portability = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'inventory_current'


