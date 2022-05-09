from django import forms
from django.contrib.auth.models import User

#from usuario.forms import ProfileForm


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

