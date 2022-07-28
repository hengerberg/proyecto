from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict
from django.urls import reverse
from usuario.models import User

from lider.models import Product



class Report(models.Model):
    STATE = [
        ('pendiente', 'Pendiente'),
        ('cancelado', 'Cancelado'),
        ('aprobado', 'Aprobado'),
        
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    # pendiente = por aprobar por el supervisor
    # cancelado = negado por el supervisores
    # aprobado = aprobado por el supervisor
    # finalizado = pagado por el supervisor
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


