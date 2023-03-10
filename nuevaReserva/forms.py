from django.forms import ModelForm
from .models import nuevaReserva, mesa
from django import forms
from django.forms import widgets

class nuevaReservaFoms(ModelForm):
    
    class Meta:
        model = nuevaReserva
        exclude = ('estado', 'apellido', 'mesa',)
        fields = '__all__'
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
        fields = '__all__'
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
        model = mesa
        fields = ['numero']
