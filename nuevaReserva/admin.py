from django.contrib import admin

from .models import estadoReserva, nuevaReserva, estadoMesa, mesaNoo, mozosPlaza, anfitriona

# Register your models here.

admin.site.register(estadoReserva)
admin.site.register(nuevaReserva)
admin.site.register(estadoMesa)
admin.site.register(mesaNoo)
admin.site.register(mozosPlaza)
admin.site.register(anfitriona)
