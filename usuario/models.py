
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

from Appgestion.settings import MEDIA_URL

class Distribuidora(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'distribuidora'
        verbose_name = 'distribuidora'
        verbose_name_plural = 'distribuidoras'

    def __str__(self):
        return self.nombre


class Profile(models.Model):
    GENRE_CHOICES = (
        ('m', 'Masculino'),
        ('f', 'Feminino'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    distributor = models.ForeignKey(Distribuidora,on_delete=models.CASCADE)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES,blank = True, null=True, verbose_name="Genero")
    avatar = models.ImageField(upload_to='profiles',blank = True, null=True, verbose_name='Imagen de Perfil')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,10}$', message="El número de teléfono debe ingresarse en el formato: '0999999999'. Se permiten hasta 10 dígitos.")
    phone = models.CharField(
        validators=[phone_regex],
        max_length=10,
        blank = True, null=True,
        verbose_name='Numero de Telefono')  # validators should be a list
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_image(self):
        if self.avatar:
            return '{}{}'.format(MEDIA_URL, self.avatar)
        return '{}{}'.format(MEDIA_URL, 'empty.png')
    
    def __str__(self):
        return '{}'.format(self.user)

