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
    nombre = models.CharField(max_length=50)
    fechaReserva = models.DateField()
    hora = models.TimeField()
    cantidadPersonas = models.PositiveIntegerField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    observaciones = models.TextField (blank = True)    
    estado = models.ForeignKey(estadoReserva, on_delete=models.DO_NOTHING)
    mesa_asignadaa = models.CharField(max_length=10, blank=True, null=True) 
    emailr = models.EmailField(max_length=254, null=True, blank= True) 
    origen_reserva = models.CharField(max_length=100, blank=True, null=True)
    

class estadoMesa(models.Model):
    estado = models.CharField(max_length=15)
    
    def __str__(self):
        return self.estado

class mesaNoo(models.Model):
    numero = models.CharField(max_length=10)
    estado = models.ForeignKey(estadoMesa, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.numero

class mesa(models.Model):
    numero = models.CharField(max_length=10)
    estado = models.ForeignKey(estadoMesa, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.numero

class incidencia(models.Model):
    fecha_incidencia = models.DateField()
    mesa_incidencia = models.CharField(max_length=10, blank=True, null=True)
    mozo_incidencia = models.CharField(max_length=50, blank=True, null=True)
    detalle_incidencia = models.TextField (blank = False, null= False)
    fecha_registro = models.DateField(auto_now_add=True)
    id_reservacion = models.CharField(max_length=20, blank=True, null=True)

class mozosPlaza(models.Model):
    nombre_mozo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_mozo

class anfitriona(models.Model):
    nombre_anfitriona = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_anfitriona
    

class plazaAlmuerzo(models.Model):
    fecha_dia = models.DateField(auto_now_add=True)
    mozo_nombre = models.CharField(max_length=50, null= True, blank= True )
    m1 = models.CharField(max_length=20, null= True, blank= True)
    r1 = models.CharField(max_length=20, null= True, blank= True)
    m2 = models.CharField(max_length=20, null= True, blank= True)
    r2 = models.CharField(max_length=20, null= True, blank= True)
    m3 = models.CharField(max_length=20, null= True, blank= True)
    r3 = models.CharField(max_length=20, null= True, blank= True)
    m4 = models.CharField(max_length=20, null= True, blank= True)
    r4 = models.CharField(max_length=20, null= True, blank= True)
    m5 = models.CharField(max_length=20, null= True, blank= True)
    r5 = models.CharField(max_length=20, null= True, blank= True)
    total = models.CharField(max_length=20, null= True, blank= True)
    plaza = models.CharField(max_length=20, null= True, blank= True) 
    nombre_anfitriona = models.CharField(max_length=50, null= True, blank= True)

class plazaCena(models.Model):
    fecha_dia = models.DateField(auto_now_add=True)
    mozo_nombre = models.CharField(max_length=50, null= True, blank= True )
    m1 = models.CharField(max_length=20, null= True, blank= True)
    r1 = models.CharField(max_length=20, null= True, blank= True)
    m2 = models.CharField(max_length=20, null= True, blank= True)
    r2 = models.CharField(max_length=20, null= True, blank= True)
    m3 = models.CharField(max_length=20, null= True, blank= True)
    r3 = models.CharField(max_length=20, null= True, blank= True)
    m4 = models.CharField(max_length=20, null= True, blank= True)
    r4 = models.CharField(max_length=20, null= True, blank= True)
    m5 = models.CharField(max_length=20, null= True, blank= True)
    r5 = models.CharField(max_length=20, null= True, blank= True)
    total = models.CharField(max_length=20, null= True, blank= True)
    plaza = models.CharField(max_length=20, null= True, blank= True)
    nombre_anfitriona = models.CharField(max_length=50, null= True, blank= True)

class plazaAlmuerzoMan(models.Model):
    fecha_dia = models.DateField(auto_now_add=True)
    n1 = models.CharField(max_length=20, null= True, blank= True)
    n2 = models.CharField(max_length=20, null= True, blank= True)
    n3 = models.CharField(max_length=20, null= True, blank= True)
    n4 = models.CharField(max_length=20, null= True, blank= True)
    n5 = models.CharField(max_length=20, null= True, blank= True)
    plaza = models.CharField(max_length=20, null= True, blank= True)

class plazaCenaMan(models.Model):
    fecha_dia = models.DateField(auto_now_add=True)
    n1 = models.CharField(max_length=20, null= True, blank= True)
    n2 = models.CharField(max_length=20, null= True, blank= True)
    n3 = models.CharField(max_length=20, null= True, blank= True)
    n4 = models.CharField(max_length=20, null= True, blank= True)
    n5 = models.CharField(max_length=20, null= True, blank= True)
    plaza = models.CharField(max_length=20, null= True, blank= True)

class incidenciaLog(models.Model):
    fecha_incidencia = models.DateField()
    detalle_incidencia = models.TextField (blank = False, null= False)
    fecha_registro = models.DateField(auto_now_add=True)   