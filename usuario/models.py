from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.forms.models import model_to_dict

from Appgestion.settings import MEDIA_URL

class User(AbstractUser):

    def toJSON(self):
        # model_to_dict sirve para obtener un diccionario a partir del 
        # modelo que se envie, tiene limitantes al convertir algunos tipos de 
        # datos como(relaciones,fecha,imagen) 
        item = model_to_dict(self, exclude=['password','user_permissions','last_login']) 
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name() # este metodo devuelve el nombre completo del usuario
        # con una lista de comprension voy iterando los grupos asociados al usuario
        item['groups'] = [{'id':g.id, 'name':g.name} for g in self.groups.all()] 
        return item

    class Meta:
        permissions = (
            # permisos de los vendedores
            ('add_seller', 'can add seller'),
            ('change_seller', 'can change seller'),
            ('del_seller', 'can delete seller'),
            ('view_seller', 'can view seller'),
            #permisos de supervisores
            ('add_supervisor', 'can add supervisor'),
            ('change_supervisor', 'can change supervisor'),
            ('del_supervisor', 'can delete supervisor'),
            ('view_supervisor', 'can view supervisor'),
            )


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
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


