from django.forms import ModelForm
from .models import nuevaReserva, mesaNoo
from django import forms
from django.forms import widgets

class nuevaReservaFoms(ModelForm):
    
    class Meta:
        model = nuevaReserva
        exclude = ('estado', 'apellido', 'mesa',)
        fields = ['nombre', 'fechaReserva', 'hora','cantidadPersonas','telefono','observaciones']
        widgets = {
            'hora' : forms.TimeInput(format='%H:%M'),
            'fechaReserva': widgets.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'fechaReserva': 'Fecha de la reserva:',
            'cantidadPersonas': 'Cantidad de personas:',
            'nombre': 'Nombres y Apellidos'
        }

class editReservaFoms(ModelForm):
    
    class Meta:
        model = nuevaReserva
        exclude = ('apellido', 'mesa',)
        fields = ['nombre', 'fechaReserva', 'hora','cantidadPersonas','telefono','observaciones']
        widgets = {
            'hora' : forms.TimeInput(format='%H:%M')
        }
        labels = {
            'fechaReserva': 'Fecha de la reserva:',
            'cantidadPersonas': 'Cantidad de personas:',
            'nombre': 'Nombres y Apellidos'
            
        }
        
class asignaMesaForm(forms.ModelForm):

    class Meta:
        model = mesaNoo
        fields = ['numero']

class formBuscarFechaHistori(forms.Form):
    fechaBuscar = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Fecha:')