from django import forms
from .models import Product, Category


class FormAddProduct(forms.ModelForm):
    """
    por realizar
    extraer las categorias creadas y mostrala en el campo select del formulario
    
    """
    name = forms.CharField(label='Nombre del Producto', max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del Producto',
            'required': 'required'
        }
    ))
    description = forms.CharField(label='Descripcion', max_length=150, min_length=10, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Descripcion',
            'required': 'required'
        }
    ))
    price_in = forms.FloatField(label='Precio para el Vendedor', widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': '$ 8.5',
            'required': 'required'
        }
    ))
    price_out = forms.FloatField(label='Precio para el cliente', widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': '$ 10',
            'required': 'required'
        }
    ))
    seller_commission = forms.FloatField(label='Comision del vendedor', widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': '$ 1.5',
            'required': 'required'
        }
    ))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),label='Categoria', widget=forms.Select(
        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    img = forms.ImageField(label='Imagen', widget=forms.ClearableFileInput(
        attrs={
            'class': 'form-control',
            'type':'file'
            
        }
    ))
    pay_commission = forms.BooleanField(label='Pagar comision', widget=forms.CheckboxInput(
        attrs={
            'class': 'form-check-input',
            'required': 'required',
            
        }
    ))
    is_active = forms.BooleanField(label='Activo', widget=forms.CheckboxInput(
        attrs={
            'class': 'form-check-input',
            'required': 'required'
        }
    ))
    
    class Meta:
        model = Product
        fields = ('name', 'description', 'price_in', 'price_out','seller_commission','category','img','pay_commission','is_active')



