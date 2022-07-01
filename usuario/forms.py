from django import forms
from django.forms import widgets
from .models import Profile,User

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('phone','genre','avatar')
        widgets = {
            'phone': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'099999999',
                    'required': True,
                    }
            ),
            'genre': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    }
            ),
            'avatar': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',
                }
            )
        }

class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'email','password'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    'class': 'form-control',
                    
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'class': 'form-control',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                    'class': 'form-control',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                    'class': 'form-control',
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Ingrese su password',
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
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'email','password','groups'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    'class': 'form-control',
                    
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'class': 'form-control',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                    'class': 'form-control',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                    'class': 'form-control',
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Ingrese su password',
                    'class': 'form-control',
                }
            ),
            'groups': forms.SelectMultiple(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'multiple':'multiple'
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

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
                u.groups.clear()
                for g in self.cleaned_data['groups']: # iteramos los grupos recibido y lo agregamos
                    u.groups.add(g)
                data['username'] = u.username # agrego a data el username para crear en la vista su perfil, inventario, etc.
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# como se va a crear un formulario nuevo utilizamos el forms.Form
class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class': 'form-control',
        'autocomplete': 'off'
    }))
 
    # sobreescribimos el metodo clean
    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            # otra forma de enviar los errores
            self._errors['Error'] = self._errors.get('Error', self.error_class())
            self._errors['Error'].append('El usuario no existe')
            #raise forms.ValidationError('El usuario no existe')
        return cleaned

    # creamos un metodo para obtener el usuario actual
    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese una contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita la contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned


# class UserFormB(forms.ModelForm):
#     username = forms.CharField(label='Usuario', max_length=15, widget=forms.TextInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Ingresa el usuario',
#             'required': 'required'
#         }
#     ))
#     first_name = forms.CharField(label='Nombres', max_length=50, min_length=2, widget=forms.TextInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Nombres',
#             'required': 'required'
#         }
#     ))
#     last_name = forms.CharField(label='Apellidos', max_length=50, min_length=2, widget=forms.TextInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Apellidos',
#             'required': 'required'
#         }
#     ))
#     email = forms.EmailField(label='Email', widget=forms.EmailInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Correo Electronico',
#             'required': 'required'
#         }
#     ))
#     password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Contraseña',
#             'id': 'password1',
#             'required': 'required'
#         }
#     ))
#     password2 = forms.CharField(label='Confirme la contraseña', widget=forms.PasswordInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Repite la contraseña',
#             'id': 'password2',
#             'required': 'required'
#         }
#     ))

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError('El Usuario ya existe')
#         return username

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('El Email ya existe')
#         return email

#     def clean_password2(self):
#         # Compruebe que las dos entradas de contraseña coincidan
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Las Contraseñas no coinciden")
#         return password2

#     def save(self, commit=True):
#         # Guarde la contraseña proporcionada en formato hash
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user