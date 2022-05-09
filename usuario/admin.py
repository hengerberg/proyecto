from django import forms
from django.contrib import admin

from .models import Profile,Distribuidora


admin.site.register(Distribuidora)

admin.site.register(Profile)

# Register your models here.

'''class FormularioCreacionUsuario(forms.ModelForm):
    """
    Un formulario para crear nuevos usuarios. Incluye todo lo requerido
    Campos, más una contraseña repetida.
    """
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id':'password1',
            'required':'required'
            }
    ))
    password2 = forms.CharField(label='Confirme la contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Repite la contraseña',
            'id':'password2',
            'required':'required'
        }
    ))

    class Meta:
        CARGOS = [
        ('jefe','Jefe'),
        ('cajero','Cajero'),
        ('mensajero','Mensajero'),
        ('supervisor','Supervisor'),
        ('vendedor','Vendedor')
    ]
        model = Usuario
        fields = ('username', 'email', 'nombres', 'apellidos','cargo','distribuidora')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Usuario'
                    }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Correo Electronico'
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Nombres'
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Apellidos'
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Telefono'
                }
            ),
            'cargo': forms.Select(choices=CARGOS,
                attrs={
                    'class': 'form-control',
                    'placeholder':'cargo'
                }
            ),
            'distribuidora': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder':'distribuidora'
                }
            )
        }
        

    def clean_password2(self):
        # Compruebe que las dos entradas de contraseña coincidan
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Guarde la contraseña proporcionada en formato hash
        username = super().save(commit=False)
        username.set_password(self.cleaned_data["password1"])
        if commit:
            username.save()
        return username

class FormularioActualizarUsuario(forms.ModelForm):
    """
    Un formulario para actualizar usuarios. Incluye todos los campos de
    El usuario, pero reemplaza el campo de contraseña con el de administrador
    Campo de visualización de hash de contraseña.
    """
    #password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = Usuario
        fields = ('username', 'password', 'nombres','apellidos','email', 'telefono', 'usuario_activo', 'cargo', 'distribuidora')
    
    def clean_password(self):
        # Independientemente de lo que proporcione el usuario, devuelva el valor inicial.
        # Esto se hace aquí, en lugar de en el campo, porque el
        # el campo no tiene acceso al valor inicial
        return self.initial["password"]

class UsuarioAdmin(BaseUserAdmin):
    #Los formularios para agregar y cambiar instancias de usuario
    form = FormularioActualizarUsuario
    add_form = FormularioCreacionUsuario
    
    # Los campos que se utilizarán para mostrar el modelo de usuario.
    # Estos anulan las definiciones en el UserAdmin base
    # que hacen referencia a campos específicos en auth.User.
    list_display = ('username', 'nombres', 'apellidos', 'email', 'telefono', 'cargo','distribuidora')
    #filtro de busqueda
    list_filter = ('usuario_activo',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informacion Personal', {'fields': ('email','nombres', 'apellidos', 'telefono','distribuidora')}),
        ('Permisos', {'fields': ('usuario_activo','cargo','usuario_administrador')}),
    )
    # add_fieldsets no es un atributo estándar de ModelAdmin. UserAdmin
    # anula get_fieldsets para usar este atributo al crear un usuario.
    #campos para el registro de usuarios
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nombres', 'apellidos', 'email', 'telefono','cargo','distribuidora','password1', 'password2'),
        }),
    )
    search_fields = ('nombres',)
    ordering = ('nombres',)
    filter_horizontal = ()

class SupervisorVendedorAdmin(admin.ModelAdmin):
    list_display = ('supervisor','vendedor')
    supervisores = Usuario.objects.filter(cargo='supervisor')
    vendedor = Usuario.objects.filter(cargo='vendedor')



# Ahora registre el nuevo UserAdmin ...
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(SupervisorVendedor, SupervisorVendedorAdmin)
admin.site.register(Distribuidora)
# ... y, dado que no usamos los permisos integrados de Django,
# anular el registro del modelo de grupo de admin.
admin.site.unregister(Group)'''