from django.db import models
from django.conf import settings
from usuario.models import User

class GrupSupervisor(models.Model):

    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'supervisores')
    vendedor = models.OneToOneField(User, on_delete=models.CASCADE,related_name = 'vendedores')
    class Meta:
        verbose_name = 'grupo supervisor'
        verbose_name_plural = 'grupos supervisores'
    

