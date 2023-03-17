from django.contrib import admin

from .models import estadoReserva, nuevaReserva, estadoMesa, mesaNo

# Register your models here.

admin.site.register(estadoReserva)
admin.site.register(nuevaReserva)
admin.site.register(estadoMesa)
admin.site.register(mesaNo)
