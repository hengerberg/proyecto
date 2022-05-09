from django import forms
from django.forms import widgets
from .models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('telefono','genre','avatar')
        widgets = {
            'telefono': forms.NumberInput(
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
    
    
