from django import db
from django.db import models
from django.forms.models import model_to_dict
from django.urls.base import reverse

from usuario.models import User
from lider.models import Product, Distribuidora

# Create your models here.
class Isla(models.Model):
   
    distributor = models.ForeignKey(Distribuidora, on_delete=models.CASCADE, related_name='distribuidora')
    name = models.CharField('nombre',max_length=100)
    address = models.CharField('direccion',max_length=255)
    description = models.TextField('descripcion',max_length=255)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('detalle-isla', args=[str(self.id)])

    class Meta:
        db_table = 'isla'
        verbose_name = 'isla'
        verbose_name_plural = 'islas'
    

class UserIsla(models.Model):
    isla = models.ForeignKey(Isla, on_delete=models.CASCADE, related_name='isla')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')

    class Meta:
        db_table = 'isla_user'
        verbose_name = 'vendedor isla'
        verbose_name_plural = 'vendedores islas'

    def __str__(self):
        return 'isla: {} vendedor: {}'.format(self.isla, self.user)

class SalesIsla(models.Model):
    OPERADORAS_CHOICES = [
        ('claro', 'Claro'),
        ('cnt', 'Cnt'),
        ('movistar', 'Movistar'),
    ]
    isla = models.ForeignKey(Isla, on_delete=models.CASCADE, related_name='saleisla')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'vendedor')
    name = models.CharField(max_length=100, blank= True, null = True)
    ci = models.IntegerField(blank = True, null=True)
    min = models.IntegerField()
    icc = models.IntegerField()
    chip = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'chip')
    nip = models.IntegerField(blank = True, null = True)
    operadora = models.CharField(max_length=20,choices=OPERADORAS_CHOICES,blank = True, null = True)
    nota = models.TextField(max_length=255, blank = True, null = True)

    class Meta:
        db_table = 'sales_isla'
        verbose_name = 'venta islas'
        verbose_name_plural = 'ventas islas'

    def toJSON(self):
        item = model_to_dict(self)
        item['isla'] = self.isla
        item['user'] = self.user.first_name + ' ' + self.user.last_name
        item['name'] = self.name
        item['ci'] = format(self.ci)
        item['min'] = format(self.min)
        item['icc'] = format(self.icc)
        item['chip'] = self.chip.name
        item['nip'] = format(self.nip)
        item['operadora'] = self.operadora
        item['nota'] = self.nota
        return item
