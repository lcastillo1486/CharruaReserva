from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class estadoReserva(models.Model):
    estado = models.CharField(max_length=15)

    def __str__(self):
        return self.estado

class nuevaReserva(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    telefono_regex = RegexValidator(regex= r'^\+?1?\d{9,15}$', message ="Formato incorrecto")
    nombre = models.CharField(max_length=20)
    fechaReserva = models.DateField()
    hora = models.TimeField()
    cantidadPersonas = models.PositiveIntegerField()
    telefono = models.CharField(validators=[telefono_regex],max_length=9, blank=True, null=True)
    observaciones = models.TextField (blank = True)    
    estado = models.ForeignKey(estadoReserva, on_delete=models.DO_NOTHING)
    mesa = models.CharField(max_length=10, blank=True, null=True)
    
class estadoMesa(models.Model):
    estado = models.CharField(max_length=15)
    
    def __str__(self):
        return self.estado

class mesa(models.Model):
    numero = models.CharField(max_length=10)
    estado = models.ForeignKey(estadoMesa, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.numero





    