from django.forms import ModelForm
from .models import nuevaReserva, mesaNoo, incidencia
from django import forms
from django.forms import widgets

class nuevaReservaFoms(ModelForm):
    
    class Meta:
        model = nuevaReserva
        exclude = ('estado', 'apellido', 'mesa',)
        fields = ['nombre', 'fechaReserva', 'hora','cantidadPersonas','telefono','emailr','observaciones']
        widgets = {
            'hora' : forms.TimeInput(format='%H:%M'),
            'fechaReserva': widgets.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'fechaReserva': 'Fecha de la reserva:',
            'cantidadPersonas': 'Cantidad de personas:',
            'nombre': 'Nombres y Apellidos',
            'emailr': 'Correo'
        }

class editReservaFoms(ModelForm):
    
    class Meta:
        model = nuevaReserva
        exclude = ('apellido', 'mesa',)
        fields = ['nombre', 'fechaReserva', 'hora','cantidadPersonas','telefono','emailr','observaciones'] 
        widgets = {
            'hora' : forms.TimeInput(format='%H:%M')
        }
        labels = {
            'fechaReserva': 'Fecha de la reserva:',
            'cantidadPersonas': 'Cantidad de personas:',
            'nombre': 'Nombres y Apellidos',
            'emailr': 'Correo'
            
        }
        
class asignaMesaForm(forms.ModelForm):

    class Meta:
        model = mesaNoo
        fields = ['numero']

class formBuscarFechaHistori(forms.Form):
    fechaBuscar = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Fecha:')

class formBuscarIncidencia(forms.Form):
    fechaBIncidencia = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='')

class formIncidencia(ModelForm):

    class Meta:
        model = incidencia
        fields = '__all__'
        exclude = ('fecha_registro',)
        widgets = {
            'fecha_incidencia': widgets.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'fecha_incidencia':'Fecha de incidencia:',
            'mesa_incidencia':'Mesa de incidencia:',
            'mozo_incidencia':'Mozo de incidencia',
            'detalle_incidencia':'Detalle de incidencia:'
        }