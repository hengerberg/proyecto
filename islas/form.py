from django import forms

from .models import Isla



class IslaCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # para agregar widget a todos los elementos del formulario
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Isla
        fields= '__all__'
        widgets={
            'name': forms.TextInput(attrs={
                'placeholder':'Nombre de la Isla',
                'required': True,
            }),
            'address': forms.TextInput(attrs={
                'placeholder':'Dirección de la Isla',
            }),
            'description': forms.Textarea(attrs={
                'placeholder':'Descripción de la Isla',
            }),
        }
        exclude = ['distributor']

    def save(self,distributor = False,commit=True):
        data = {} # creamos el diccionario para saber si tiene errores o no
        form = super() # recuperamos la informacion del formulario
        try:
            if form.is_valid():
                if commit:
                    form.save()
                else:
                    # If not committing, add a method to the form to allow deferred
                    # saving of m2m data.
                    data = form.save(commit=False)
                    data.distributor_id = distributor
                    data.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

