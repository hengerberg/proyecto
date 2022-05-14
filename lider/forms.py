from django import forms
from .models import Product, Category

class FormAddProduct(forms.ModelForm):
    """
    por realizar
    extraer las categorias creadas y mostrala en el campo select del formulario
    
    """
   
    class Meta:
        model = Product
        fields = ('name', 'description', 'price_in', 'price_out','seller_commission','category','img','pay_commission','is_active')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Nombre del Producto',
                    'required': True,
                    }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    }
            ),
            'price_in':forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'$ 2.5',
                    'required': True
                }
            ),
            'price_out':forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'$ 5',
                    'required': True
                }
            ),
            'seller_commission':forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'$ 1.5',
                    'required': True
                }
            ),
            'category':forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'img':forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',
                    'type':'file'
                }
            ),
            'pay_commission':forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'is_active':forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

        }


