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
     path('verPlaza/', views.verPlaza),
    path('guardarPlazaAlmuerzo/', views.guardaPlazaAlm),
    path('guardarPlazaCena/', views.guardaPlazaCena),
    path('historicoPlazas/', views.guardaPlazaCena),

]