from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict
from django.urls import reverse
from Appgestion.settings import MEDIA_URL

from usuario.models import Distribuidora


class Category(models.Model):
    name = models.CharField('categoria', max_length=100)

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



class Report(models.Model):
    STATE = [
        ('pendiente', 'Pendiente'),
        ('cancelado', 'Cancelado'),
        ('aprobado', 'Aprobado'),
        
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    state = models.CharField(max_length=20, choices=STATE, default = 'pendiente')
    subtotal = models.FloatField()
    commission_paid = models.FloatField(default=0.00)
    commission_receivable = models.FloatField(default=0.00)
    discount = models.FloatField()
    total = models.FloatField()
    
    class Meta:
        db_table = 'report'
        verbose_name = 'report'
        verbose_name_plural = 'reports'

    def get_absolute_url(self):
        """
        devuelve el url a una instancia particular del reporte_detalle
        """
        return reverse('report-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.user.username
    
    def toJSON(self):
        item = model_to_dict(self) # permite devolver todos los parametros del modelo en un diccionario
        item['user'] = self.user.first_name + ' ' + self.user.last_name
        item['user_id'] = self.user.id
        item['date'] = self.date.strftime('%Y-%m-%d')
        item['state'] = self.state
        item['subtotal'] = format(self.subtotal, '.2f')
        item['commission_paid'] = format(self.commission_paid, '.2f')
        item['commission_receivable'] = format(self.commission_receivable, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total'] = format(self.total, '.2f')
        item['det'] = [i.toJSON() for i in self.reportdetail_set.all()]
        return item
    


class ReportDetail(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(default=0.00)
    commission_paid = models.FloatField(default=0.00)
    commission_receivable = models.FloatField(default=0.00)
    total = models.FloatField(default=0.00)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['report'])
        item['product'] = self.product.toJSON()
        item['commission_paid'] = format(self.commission_paid, '.2f')
        item['commission_receivable'] = format(self.commission_receivable, '.2f')
        item['price'] = format(self.price, '.2f')
        item['total'] = format(self.total, '.2f')
        return item


