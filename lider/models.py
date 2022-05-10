from django.db import models
from django.forms.models import model_to_dict

from Appgestion.settings import MEDIA_URL
from usuario.models import Distribuidora
# Create your models here.


class Category(models.Model):
    name = models.CharField('categoria', max_length=100)
    distributor = models.ForeignKey(Distribuidora, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def toJSON(self):
        item = model_to_dict(self)
        return item



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distribuidora, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='products',blank = True, null=True, verbose_name='Imagen de producto')
    name = models.CharField('nombre del producto',max_length=100)
    description = models.CharField('descripcion del producto',max_length=255)
    price_in = models.FloatField('precio para el vendedor')
    price_out = models.FloatField('precio para el cliente')
    seller_commission = models.FloatField('comision del vendedor')
    pay_commission = models.BooleanField('Pagar comision')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.category.toJSON()
        item['img'] = self.get_image()
        item['price_in'] = format(self.price_in, '.2f')
        item['price_out'] = format(self.price_out, '.2f')
        item['seller_commission'] = format(self.seller_commission, '.2f')
        item['pay_commission'] = self.pay_commission
        
        return item
    
    def get_image(self):
        if self.img:
            return '{}{}'.format(MEDIA_URL, self.img)
        return '{}{}'.format(MEDIA_URL, 'prod-empty.jpg')

    def __str__(self):
        return self.name

