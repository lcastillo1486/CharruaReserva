from django.urls import path
from nuevaReserva import views

urlpatterns = [
    path('nuevaReserva/', views.creaNuevaReserva),
    path('enEspera/', views.listadoEnEspera, name ='enespera'),
    #path('enProceso/', views.listadoEnProceso),
    path('historico/', views.listadoCompletado),
    path('reservasDelDia/', views.listadoDelDia, name='delDia'),
    path('editarReserva/<int:id>', views.editarReserva),
    path('cambiarEstadoReserva/<int:id>', views.cambioEstadoReserva),
    #path('cargaAsignacionMesa/<int:id>', views.cargaAsignarMesa),
    path('cambiarEstadoAnulado/<int:id>', views.cambiaEstadoAnulado),
    path('cambiarEstadoShow/<int:id>', views.cambiaEstadoNoShow),
    path('estadoActual/', views.estadoActual),
    path('guardarMesa/<int:id>', views.guardarMesa),
    path('muestraCena/', views.muentraCena),
    path('muestraTarde/', views.muentraTarde),
    path('exportarExcel/', views.exportaExcel),
    path('buscarFecha/', views.buscaHistoricoFecha),
    path('exportarExcelHist/', views.exportaExcelHistorico),
    path('libroIncidencias/', views.agregarIncidencia),
    path('buscaIncidencias/', views.buscarIncidencias),
    path('verPlaza/', views.verPlaza, name ='verPlaza'),
    path('guardarPlazaAlmuerzo/', views.guardaPlazaAlm, name='guardaalmuerzo'),
    path('guardarPlazaCena/', views.guardaPlazaCena),
    path('historicoPlazas/', views.verHistoricoPlaza, name ='historicoP'),
    path('mesaManAlm/<str:nmesa>', views.controlMesaManAlm),
    path('mesaManCen/<str:nmesa>', views.controlMesaManCen),
    path('libroIncidenciasLog/', views.agregarIncidenciaLog),
    path('buscaIncidenciasLog/', views.buscarIncidenciasLog),
    path('agregarIncidReser/<int:id>', views.agregarIncidenciaReserva),
    path('guardarIncidReser/', views.guardarIncidenciaReserva),
    path('calculardia/', views.calculardia),
    path('verplazasfds/', views.verplazafds, name='verPlazasfds'),
    path('mesaManCenfds/<str:nmesa>', views.controlMesaManCenfds),
    path('mesaManAlmfds/<str:nmesa>', views.controlMesaManAlmfds),
    path('estadisticas/', views.estadisticas),
    path('guardarPlazaAlmuerzofds/', views.guardaPlazaAlmfds, name='guardaalmuerzofds'),
    path('guardarPlazaCenafds/', views.guardaPlazaCenafds, name='guardacenafds'),
    path('encuesta/', views.muestraencuesta),
    path('guardaencuesta/', views.guardarencuesta),
    path('gracias/', views.muestragracias),





]