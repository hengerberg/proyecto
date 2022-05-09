from django import forms


from .models import Report


class ReportForm(forms.ModelForm):
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
