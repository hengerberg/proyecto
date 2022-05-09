from django.db import models
from django.conf import settings
#from usuario.models import Usuario

class GrupSupervisor(models.Model):

    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name = 'supervisores')
    vendedor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name = 'vendedores')
    class Meta:
        verbose_name = 'grupo supervisor'
        verbose_name_plural = 'grupos supervisores'
    

