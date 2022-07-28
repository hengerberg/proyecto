from django import forms
from django.contrib.auth.models import Group

from usuario.models import User
from vendedor.models import Report

#from usuario.forms import ProfileForm


class SellerCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'email','password'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese  nombres',
                    'class': 'form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'class': 'form-control',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el email',
                    'class': 'form-control',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el username',
                    'class': 'form-control',
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Ingrese su Contraseña',
                    'class': 'form-control',
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff','groups']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                #print(self.cleaned_data['groups']) # compruebo que si esta llegando la informacion de los grupos
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                group = Group.objects.get(name='vendedor')
                u.groups.add(group)
                data['username'] = u.username # agrego a data el username para crear en la vista su perfil, inventario, etc.
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SellerUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingresa el usuario',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombres',
                    
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellidos',
                    
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo Electronico',
                    
                }
            )
        }


class SalesCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # para agregar widget a todos los elementos del formulario
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        # agregar wigets a los componentes
        # forma 1
        """self.fields['date'].widget.attrs['class'] = 'form-control datetimepicker-input'
        self.fields['date'].widget.attrs['id'] = 'date'
        self.fields['date'].widget.attrs['data-target'] = '#date'
        self.fields['date'].widget.attrs['data-toggle'] = 'datetimepicker'"""

        # forma 2
        """self.fields['date'].widget.attrs = {
            'class':'form-control datetimepicker-input',
            'id':'date',
            'data-target':'#date',
            'data-toggle':'datetimepicker'
        }"""
    commission_paid = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'readonly': True,
        }
    ))
    commission_receivable = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'readonly': True,
        }
    ))
    class Meta:
        model=Report
        fields=('date', 'subtotal', 'discount', 'total')
        widgets={
            'date': forms.DateInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'id': 'date',
                    'data-target': '#date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,

            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
            }),
            'discount': forms.TextInput(attrs={

            }),
        }



class FormularioCrearVendedor(forms.ModelForm):
    username = forms.CharField(label='Usuario', max_length=15, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa el usuario',
            'required': 'required'
        }
    ))
    first_name = forms.CharField(label='Nombres', max_length=50, min_length=2, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nombres',
            'required': 'required'
        }
    ))
    last_name = forms.CharField(label='Apellidos', max_length=50, min_length=2, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos',
            'required': 'required'
        }
    ))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Correo Electronico',
            'required': 'required'
        }
    ))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'password1',
            'required': 'required'
        }
    ))
    password2 = forms.CharField(label='Confirme la contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Repite la contraseña',
            'id': 'password2',
            'required': 'required'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El Usuario ya existe')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El Email ya existe')
        return email

    def clean_password2(self):
        # Compruebe que las dos entradas de contraseña coincidan
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las Contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Guarde la contraseña proporcionada en formato hash
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user