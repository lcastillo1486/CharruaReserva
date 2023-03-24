from django.shortcuts import render, HttpResponse, redirect
from .forms import nuevaReservaFoms, editReservaFoms, asignaMesaForm, formBuscarFechaHistori, formIncidencia, formBuscarIncidencia
from django.contrib import messages
from .models import nuevaReserva, mesaNoo, estadoMesa, incidencia,  mozosPlaza, plazaAlmuerzo, anfitriona, plazaCena,  mozosPlaza, plazaAlmuerzo, anfitriona, plazaAlmuerzo, anfitriona, plazaCena
from django.db import models
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import openpyxl
# Create your views here.

@login_required
def creaNuevaReserva(request):

    form = nuevaReservaFoms()
    context = {'form_reserva': form}

    if request.method == 'POST':
        form = nuevaReservaFoms(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.estado_id = 1
            a.save()
            
            return redirect('/reservasDelDia/')
        else:
            
            return render(request, 'nuevaReserva.html', {'form_reserva': form})

    return render(request, 'nuevaReserva.html', context)
@login_required
def listadoEnEspera(request):

    fecha_actual = datetime.now().date()

    cuenta_atendido = nuevaReserva.objects.filter(estado_id = 2, fechaReserva = fecha_actual).count()
    cuenta_anulado = nuevaReserva.objects.filter(estado_id = 3, fechaReserva = fecha_actual).count()
    cuenta_noshow = nuevaReserva.objects.filter(estado_id = 4, fechaReserva = fecha_actual).count()

    
    fecha_actual = datetime.now().date()

    enEspera = nuevaReserva.objects.filter(estado_id = 1).order_by('fechaReserva')
    cuenta_enEspera = nuevaReserva.objects.filter(estado_id = 1).count()
    return render(request, 'listadoEnEspera.html', {"listaEspera": enEspera, "totalEspera":cuenta_enEspera})
@login_required
def listadoDelDia(request):
    
    fecha_actual = datetime.now().date()

    cuenta_atendido = nuevaReserva.objects.filter(estado_id = 2, fechaReserva = fecha_actual).count()
    cuenta_anulado = nuevaReserva.objects.filter(estado_id = 3, fechaReserva = fecha_actual).count()
    cuenta_noshow = nuevaReserva.objects.filter(estado_id = 4, fechaReserva = fecha_actual).count()

    deldia = nuevaReserva.objects.filter(fechaReserva = fecha_actual ).order_by('hora')
    cuenta_deldia = nuevaReserva.objects.filter(estado_id = 1, fechaReserva = fecha_actual ).count()
    totalClientesAten = nuevaReserva.objects.filter(fechaReserva = fecha_actual, estado_id = 2).aggregate(Sum('cantidadPersonas'))
    totalpersonas = (totalClientesAten['cantidadPersonas__sum'])
    return render(request, 'reservasDelDia.html', {"listaEspera": deldia, "totalDia":cuenta_deldia, 'fechaHoy':fecha_actual, 'totalAtendido':cuenta_atendido,
    'totalAnulado':cuenta_anulado, 'totalNoshow':cuenta_noshow, "totalPersonas":totalpersonas})
@login_required
def listadoEnProceso(request):
    en_proceso = nuevaReserva.objects.filter(estado_id = 2)
    cuenta_en_proceso = nuevaReserva.objects.filter(estado_id = 2).count()
    return render(request, 'listadoEnProceso.html', {"listaEnProceso": en_proceso, "totalProceso":cuenta_en_proceso})
@login_required
def listadoCompletado(request):
    formBuscar = formBuscarFechaHistori()
    completado = nuevaReserva.objects.all().order_by('-fechaReserva')
    cuenta_completado = nuevaReserva.objects.filter(estado_id = 2).count()
    return render(request, 'listadoHistorico.html', {"listaCompletado": completado, "totalCompletado":cuenta_completado, "formBusca":formBuscar})
@login_required
def editarReserva(request, id):

    editCurso = nuevaReserva.objects.get(id = id)
    form = editReservaFoms(instance=editCurso)

    # if editCurso.estado_id != 1:
    
    #      return HttpResponse('Esta reserva ya ha sido procesada. No se puede modificar')

    if request.method == 'POST':

        form = editReservaFoms(request.POST,instance=editCurso)
        if form.is_valid:
            form.save()
            return redirect('/reservasDelDia/') 

    editCurso = nuevaReserva.objects.get(id = id)
    form = editReservaFoms(instance=editCurso)

    return render(request,'editarReserva.html',{"form":form})
@login_required
def cambioEstadoReserva(request, id):
    
    cambiaEstado = nuevaReserva.objects.get(id = id)
    cambiaEstado.estado_id = 2
    cambiaEstado.save()    
    
    return redirect('/reservasDelDia/')
@login_required
def cambiaEstadoAnulado(request, id):
    cambiaEstadoAnulado = nuevaReserva.objects.get(id = id)
    cambiaEstadoAnulado.estado_id = 3
    cambiaEstadoAnulado.save()    
    
    return redirect('/reservasDelDia/')
@login_required
def cambiaEstadoNoShow(request, id):

    cambiaEstadoShow = nuevaReserva.objects.get(id = id)
    cambiaEstadoShow.estado_id = 4
    cambiaEstadoShow.save()    
    
    return redirect('/reservasDelDia/')
@login_required
def cargaAsignarMesa(request, id):
    form = asignaMesaForm()
    reserva = nuevaReserva.objects.filter(id = id)
    return render(request,'asignaMesa.html',{"listaReserva":reserva, 'form':form})
@login_required
def estadoActual(request):

    fecha_actual = datetime.now().date()

    cuenta_enEspera = nuevaReserva.objects.filter(fechaReserva = fecha_actual).count()
    cuenta_en_proceso = nuevaReserva.objects.filter(estado_id = 2, fechaReserva = fecha_actual).count()
    cuenta_completado = nuevaReserva.objects.filter(estado_id = 3, fechaReserva = fecha_actual).count()
    cuenta_cancelada = nuevaReserva.objects.filter(estado_id = 4, fechaReserva = fecha_actual).count()

    ratio_progreso = round((cuenta_en_proceso/cuenta_enEspera)*100,2)
    ratio_completadas = round((cuenta_completado/cuenta_enEspera)*100,2)
    ratio_faltante = round(((cuenta_en_proceso + cuenta_completado)/cuenta_enEspera)*100,2)

    data = {'porcentajles': [ratio_progreso,ratio_completadas, ratio_faltante],'etiqueta':['progreso','completo','faltante']}


    return render(request, 'estadoActual.html', {'cantidadEspera':cuenta_enEspera, 'cantidadProgreso':cuenta_en_proceso, 'cantidadCompletada':cuenta_completado,
    'cantidadCancelada':cuenta_cancelada, 'ratioProgreso':ratio_progreso, 'ratioCompletado':ratio_completadas, 'ratioFaltante':ratio_faltante, 'data':data})
@login_required
def guardarMesa(request, id):
    
    if request.method == 'POST':
        mesa = request.POST.get('mesa')
        cambiaMesa = nuevaReserva.objects.get(id = id)
        cambiaMesa.mesa_asignadaa = mesa
        cambiaMesa.save()

        return redirect('delDia')
@login_required
def muentraCena(request):

    fecha_actual = datetime.now().date()

    cuenta_atendido = nuevaReserva.objects.filter(estado_id = 2, fechaReserva = fecha_actual).count()
    cuenta_anulado = nuevaReserva.objects.filter(estado_id = 3, fechaReserva = fecha_actual).count()
    cuenta_noshow = nuevaReserva.objects.filter(estado_id = 4, fechaReserva = fecha_actual).count()

    deldia = nuevaReserva.objects.filter(fechaReserva = fecha_actual, hora__gt = '17:30' ).order_by('hora')

    totalClientesAten = nuevaReserva.objects.filter(fechaReserva = fecha_actual, estado_id = 2).aggregate(Sum('cantidadPersonas'))
    totalpersonas = (totalClientesAten['cantidadPersonas__sum'])

    cuenta_deldia = nuevaReserva.objects.filter(estado_id = 1, fechaReserva = fecha_actual ).count()
    return render(request, 'reservasDelDia.html', {"listaEspera": deldia, "totalDia":cuenta_deldia, 'fechaHoy':fecha_actual, 'totalAtendido':cuenta_atendido,
    'totalAnulado':cuenta_anulado, 'totalNoshow':cuenta_noshow, "totalPersonas":totalpersonas })
@login_required
def muentraTarde(request):

    fecha_actual = datetime.now().date()

    cuenta_atendido = nuevaReserva.objects.filter(estado_id = 2, fechaReserva = fecha_actual).count()
    cuenta_anulado = nuevaReserva.objects.filter(estado_id = 3, fechaReserva = fecha_actual).count()
    cuenta_noshow = nuevaReserva.objects.filter(estado_id = 4, fechaReserva = fecha_actual).count()

    deldia = nuevaReserva.objects.filter(fechaReserva = fecha_actual, hora__lt = '17:30' ).order_by('hora')
    totalClientesAten = nuevaReserva.objects.filter(fechaReserva = fecha_actual, estado_id = 2).aggregate(Sum('cantidadPersonas'))
    totalpersonas = (totalClientesAten['cantidadPersonas__sum'])

    cuenta_deldia = nuevaReserva.objects.filter(estado_id = 1, fechaReserva = fecha_actual ).count()
    return render(request, 'reservasDelDia.html', {"listaEspera": deldia, "totalDia":cuenta_deldia, 'fechaHoy':fecha_actual, 'totalAtendido':cuenta_atendido,
    'totalAnulado':cuenta_anulado, 'totalNoshow':cuenta_noshow, "totalPersonas":totalpersonas })
@login_required
def exportaExcel(request):

    fecha_actual = datetime.now().date()
    deldia = nuevaReserva.objects.filter(fechaReserva = fecha_actual ).order_by('hora')
    
    #crea nuevo libro
    wb = openpyxl.Workbook()

    hoja = wb.active

    hoja['A1'] = 'Hora'
    hoja['B1'] = 'Cliente'
    hoja['C1'] = 'Cantidad Personas'
    hoja['D1'] = 'Observaciones'
    hoja['E1'] = 'Fecha'

    row = 2

    for i in deldia:
        hoja.cell(row, 1, i.hora)
        hoja.cell(row, 2, i.nombre)
        hoja.cell(row, 3, i.cantidadPersonas)
        hoja.cell(row, 4, i.observaciones)
        hoja.cell(row, 5, fecha_actual)
        row += 1
    
    response = HttpResponse(content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reservasdia.xlsx"'

    wb.save(response)

    return response
@login_required
def buscaHistoricoFecha(request):

    formBuscar = formBuscarFechaHistori(request.POST)
    
    if request.method == 'POST':
        if formBuscar.is_valid():
            b = formBuscar.cleaned_data['fechaBuscar']
            completado = nuevaReserva.objects.filter(fechaReserva = b).order_by('-fechaReserva')
            cuenta_completado = nuevaReserva.objects.filter(estado_id = 2).count()
            return render(request, 'listadoHistorico.html', {"listaCompletado": completado, "totalCompletado":cuenta_completado, "formBusca":formBuscar})
@login_required
def exportaExcelHistorico(request):

    completado = nuevaReserva.objects.all().order_by('-fechaReserva')
    
    #crea nuevo libro
    wb1 = openpyxl.Workbook()

    hoja = wb1.active

    hoja['A1'] = 'Cliente'
    hoja['B1'] = 'Teléfono'
    hoja['C1'] = 'Correo'
    hoja['D1'] = 'Fecha de Reserva'
    hoja['E1'] = 'Hora'
    hoja['F1'] = 'Cantidad de Personas'
    hoja['G1'] = 'Observaciones'
    hoja['H1'] = 'Estado'

    row = 2

    for i in completado:
        hoja.cell(row, 1, i.nombre)
        hoja.cell(row, 2, i.telefono)
        hoja.cell(row, 3, i.emailr)
        hoja.cell(row, 4, i.fechaReserva)
        hoja.cell(row, 5, i.hora)
        hoja.cell(row, 6, i.cantidadPersonas)
        hoja.cell(row, 7, i.observaciones)
        hoja.cell(row, 8, str(i.estado))
        row += 1
    
    response = HttpResponse(content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="HistoricoReservas.xlsx"'

    wb1.save(response)

    return response
@login_required
def agregarIncidencia(request):

    bi = incidencia.objects.all().order_by('-fecha_incidencia')
    form = formIncidencia()
    form_buscar = formBuscarIncidencia()

    if request.method == 'POST':
        form = formIncidencia(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('/libroIncidencias/')
        else:
            
            return render(request, 'incidencia.html', {'form_inciden':form, 'formBuscarInciden':form_buscar, 'listadoInciden':bi})
    
    return render(request, 'incidencia.html', {'form_inciden':form, 'formBuscarInciden':form_buscar, 'listadoInciden':bi})
@login_required
def buscarIncidencias(request):

    form = formIncidencia()
    form_buscar = formBuscarIncidencia()

    form_buscar = formBuscarIncidencia(request.POST)
    if request.method == 'POST':
        if form_buscar.is_valid():
            b = form_buscar.cleaned_data['fechaBIncidencia']
            bi = incidencia.objects.filter(fecha_incidencia = b).order_by('-fecha_incidencia')
            return render(request, 'incidencia.html', {'form_inciden':form, 'formBuscarInciden':form_buscar, 'listadoInciden':bi})
    else:
        return redirect('/libroIncidencias/')

def verPlaza(request):
    fecha_actual = datetime.now().date()
    mozoz_p = mozosPlaza.objects.all()
    anfitrionas = anfitriona.objects.all()

    #plaza1
    mesa1 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '1', hora__lt = '17:30').count()
    mesa2 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '2', hora__lt = '17:30').count()
    mesa3 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '3', hora__lt = '17:30').count()
    mesa6 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '6', hora__lt = '17:30').count()
    mesa6A = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '6A', hora__lt = '17:30').count()
    tota_plaza1 = mesa1 + mesa2 + mesa3 + mesa6 +  mesa6A

    #plaza2
    mesa4 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '4', hora__lt = '17:30').count()
    mesa5 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '5', hora__lt = '17:30').count()
    mesa10 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '10', hora__lt = '17:30').count()
    mesa11 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '11', hora__lt = '17:30').count()
    mesa12 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '12', hora__lt = '17:30').count()
    tota_plaza2 = mesa4 + mesa5 + mesa10 + mesa11 +  mesa12

    #plaza3
    mesa12a = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '12A', hora__lt = '17:30').count()
    mesa14 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '14', hora__lt = '17:30').count()
    mesa15 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '15', hora__lt = '17:30').count()
    mesa16 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '16', hora__lt = '17:30').count()

    tota_plaza3 = mesa12a + mesa14 + mesa15 + mesa16

    #plaza4
    mesa17 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '17', hora__lt = '17:30').count()
    mesa18 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '18', hora__lt = '17:30').count()
    mesa8 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '8', hora__lt = '17:30').count()
    mesa9 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '9', hora__lt = '17:30').count()
    mesa34 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '34', hora__lt = '17:30').count()
    tota_plaza4 = mesa17 + mesa18 + mesa8 + mesa9 +  mesa34

    #plaza5
    mesa26 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '26', hora__lt = '17:30').count()
    mesa19 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '19', hora__lt = '17:30').count()
    mesa20 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '20', hora__lt = '17:30').count()
    mesa21 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '21', hora__lt = '17:30').count()

    tota_plaza5 = mesa26 + mesa19 + mesa20 + mesa21 

    #plaza6
    mesa22 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '22', hora__lt = '17:30').count()
    mesa30 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '30', hora__lt = '17:30').count()
    mesa31 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '31', hora__lt = '17:30').count()
    mesa32 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '32', hora__lt = '17:30').count()

    tota_plaza6 = mesa22 + mesa30 + mesa31 + mesa32

    #plaza7
    mesa27 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '27', hora__lt = '17:30').count()
    mesa28 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '28', hora__lt = '17:30').count()
    mesa29 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '29', hora__lt = '17:30').count()
    mesab3 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = 'B3', hora__lt = '17:30').count()

    tota_plaza7 = mesa27 + mesa28 + mesa29 + mesab3  

    #plaza8
    mesa35 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '35', hora__lt = '17:30').count()
    mesa36 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '36', hora__lt = '17:30').count()
    mesa37 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '37', hora__lt = '17:30').count()
    mesa38 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '38', hora__lt = '17:30').count()
    mesa39 = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '39', hora__lt = '17:30').count()
    tota_plaza8 = mesa35 + mesa36 + mesa37 + mesa38 +  mesa39

    #plaza9
    mesajp = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = 'JP', hora__lt = '17:30').count()
    tota_plaza9 = mesajp 

    #plaza10
    mesabelua = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = 'BELUA', hora__lt = '17:30').count()
    tota_plaza10 = mesabelua

    #plaza1c
    mesa1c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '1', hora__gt = '17:30').count()
    mesa2c= nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '2', hora__gt = '17:30').count()
    mesa3c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '3', hora__gt = '17:30').count()
    mesa6c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '6', hora__gt = '17:30').count()
    mesa6Ac = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '6A', hora__gt = '17:30').count()
    tota_plaza1c = mesa1c + mesa2c + mesa3c + mesa6c +  mesa6Ac

    #plaza2c
    mesa4c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '4', hora__gt = '17:30').count()
    mesa5c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '5', hora__gt = '17:30').count()
    mesa10c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '10', hora__gt = '17:30').count()
    mesa11c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '11', hora__gt = '17:30').count()
    mesa12c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '12', hora__gt = '17:30').count()
    tota_plaza2c = mesa4c + mesa5c + mesa10c + mesa11c +  mesa12c

    #plaza3c
    mesa12ac = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '12A', hora__gt = '17:30').count()
    mesa14c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '14', hora__gt = '17:30').count()
    mesa15c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '15', hora__gt = '17:30').count()
    mesa16c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '16', hora__gt = '17:30').count()

    tota_plaza3c = mesa12ac + mesa14c + mesa15c + mesa16c

    #plaza4c
    mesa17c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '17', hora__gt = '17:30').count()
    mesa18c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '18', hora__gt = '17:30').count()
    mesa8c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '8', hora__gt = '17:30').count()
    mesa9c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '9', hora__gt = '17:30').count()
    mesa34c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '34', hora__gt = '17:30').count()
    tota_plaza4c = mesa17c + mesa18c + mesa8c + mesa9c +  mesa34c

    #plaza5c
    mesa26c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '26', hora__gt = '17:30').count()
    mesa19c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '19', hora__gt = '17:30').count()
    mesa20c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '20', hora__gt = '17:30').count()
    mesa21c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '21', hora__gt = '17:30').count()

    tota_plaza5c = mesa26c + mesa19c + mesa20c + mesa21c 

    #plaza6c
    mesa22c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '22', hora__gt = '17:30').count()
    mesa30c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '30', hora__gt = '17:30').count()
    mesa31c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '31', hora__gt = '17:30').count()
    mesa32c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '32', hora__gt = '17:30').count()

    tota_plaza6c = mesa22c + mesa30c + mesa31c + mesa32c

    #plaza7c
    mesa27c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '27', hora__gt = '17:30').count()
    mesa28c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '28', hora__gt = '17:30').count()
    mesa29c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '29', hora__gt = '17:30').count()
    mesab3c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = 'B3', hora__gt = '17:30').count()

    tota_plaza7c = mesa27c + mesa28c + mesa29c + mesab3c  

    #plaza8c
    mesa35c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '35', hora__gt = '17:30').count()
    mesa36c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '36', hora__gt = '17:30').count()
    mesa37c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '37', hora__gt = '17:30').count()
    mesa38c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '38', hora__gt = '17:30').count()
    mesa39c = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = '39', hora__gt = '17:30').count()
    tota_plaza8c = mesa35c + mesa36c + mesa37c + mesa38c +  mesa39c

    #plaza9c
    mesajpc = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = 'JP', hora__gt = '17:30').count()
    tota_plaza9c = mesajpc 

    #plaza10c
    mesabeluac = nuevaReserva.objects.filter(fechaReserva = fecha_actual, mesa_asignadaa = 'BELUA', hora__gt = '17:30').count()
    tota_plaza10c = mesabeluac

    return render(request, 'plazas.html',{'listaMozos':mozoz_p, 'meza1':mesa1, 'meza2':mesa2,'meza3':mesa3,'meza6':mesa6, 'meza6A':mesa6A, 
                                          'totalplaza1': tota_plaza1,'meza4':mesa4, 'meza5':mesa5,'meza10':mesa10,'meza11':mesa11, 'meza12':mesa12, 
                                          'totalplaza2': tota_plaza2,'meza12a':mesa12a, 'meza14':mesa14,'meza15':mesa15,'meza16':mesa16, 
                                          'totalplaza3': tota_plaza3, 'meza17':mesa17, 'meza18':mesa18,'meza8':mesa8,'meza9':mesa9, 'meza34':mesa34, 
                                          'totalplaza4': tota_plaza4, 'meza26':mesa26, 'meza19':mesa19,'meza20':mesa20,'meza21':mesa21, 
                                          'totalplaza5': tota_plaza5, 'meza22':mesa22, 'meza30':mesa30,'meza31':mesa31,'meza32':mesa32, 
                                          'totalplaza6': tota_plaza6, 'meza27':mesa27, 'meza28':mesa28,'meza29':mesa29,'mezab3':mesab3, 
                                          'totalplaza7': tota_plaza7, 'meza35':mesa35, 'meza36':mesa36,'meza37':mesa37,'meza38':mesa38, 'meza39':mesa39, 
                                          'totalplaza8': tota_plaza8, 'mezajp':mesajp, 
                                          'totalplaza9': tota_plaza9, 'mezabelua':mesabelua,
                                          'meza1c':mesa1c, 'meza2c':mesa2c,'meza3c':mesa3c,'meza6c':mesa6c, 'meza6Ac':mesa6Ac, 
                                          'totalplaza1c': tota_plaza1c,'meza4c':mesa4c, 'meza5c':mesa5c,'meza10c':mesa10c,'meza11c':mesa11c, 'meza12c':mesa12c, 
                                          'totalplaza2c': tota_plaza2c,'meza12ac':mesa12ac, 'meza14c':mesa14c,'meza15c':mesa15c,'meza16c':mesa16c, 
                                          'totalplaza3c': tota_plaza3c, 'meza17c':mesa17c, 'meza18c':mesa18c,'meza8c':mesa8c,'meza9c':mesa9c, 'meza34c':mesa34c, 
                                          'totalplaza4c': tota_plaza4c, 'meza26c':mesa26c, 'meza19c':mesa19c,'meza20c':mesa20c,'meza21c':mesa21c, 
                                          'totalplaza5c': tota_plaza5c, 'meza22c':mesa22c, 'meza30c':mesa30c,'meza31c':mesa31c,'meza32c':mesa32c, 
                                          'totalplaza6c': tota_plaza6c, 'meza27c':mesa27c, 'meza28c':mesa28c,'meza29c':mesa29c,'mezab3c':mesab3c, 
                                          'totalplaza7c': tota_plaza7c, 'meza35':mesa35c, 'meza36':mesa36c,'meza37c':mesa37c,'meza38c':mesa38c, 'meza39c':mesa39c, 
                                          'totalplaza8c': tota_plaza8c, 'mezajpc':mesajpc, 
                                          'totalplaza9c': tota_plaza9c, 'mezabeluac':mesabeluac, 
                                          'totalplaza10c': tota_plaza10c, 'fecha_hoy':fecha_actual, 'listaAnfitrionas':anfitrionas})

def guardaPlazaAlm(request):
    fecha_actual = datetime.now().date()
    hora_actual = datetime.now().strftime('%H:%M')

    if plazaAlmuerzo.objects.filter(fecha_dia = fecha_actual).exists():
        return HttpResponse('Ya esta guardado')

    if hora_actual < '17:30':
        return HttpResponse('No puede guardar la plaza hasta finalizar el turno')
    


    if request.method == 'POST':

        mozo = request.POST.get('mozoplaza1')      
        m1 = request.POST.get('m1')
        r1 = request.POST.get('r1')
        m2 = request.POST.get('m2')
        r2 = request.POST.get('r2')
        m3 = request.POST.get('m3')
        r3 = request.POST.get('r3')
        m6 = request.POST.get('m6')
        r6 = request.POST.get('r6')
        m6a = request.POST.get('m6A')
        r6a = request.POST.get('r6A')
        total = request.POST.get('totalpz1')
        plaza = 'Plaza1'
        anfi = request.POST.get('anfitriona')

        plaza_dia = plazaAlmuerzo(m1 = m1, r1 = r1, m2 = m2, r2 = r2, m3 = m3, r3 = r3,
                                   m4 = m6, r4 = r6, m5 = m6a, r5 = r6a, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

        mozo = request.POST.get('mozoplaza2')      
        m4 = request.POST.get('m4')
        r4 = request.POST.get('r4')
        m5 = request.POST.get('m5')
        r5 = request.POST.get('r5')
        m10 = request.POST.get('m10')
        r10 = request.POST.get('r10')
        m11 = request.POST.get('m11')
        r11 = request.POST.get('r11')
        m12 = request.POST.get('m12')
        r12 = request.POST.get('r12')
        total = request.POST.get('totalpz2')
        plaza = 'Plaza2'
        anfi = request.POST.get('anfitriona')


        plaza_dia = plazaAlmuerzo(m1 = m4, r1 = r4, m2 = m5, r2 = r5, m3 = m10, r3 = r10, m4 = m11,
                                   r4 = r11, m5 = m12, r5 = r12, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

        mozo = request.POST.get('mozoplaza3')      
        m12a = request.POST.get('m12A')
        r12 = request.POST.get('r12')
        m14 = request.POST.get('m14')
        r14 = request.POST.get('r14')
        m15 = request.POST.get('m15')
        r15 = request.POST.get('r15')
        m16 = request.POST.get('m16')
        r16 = request.POST.get('r16')
        total = request.POST.get('totalpz3')
        plaza = 'Plaza3'
        anfi = request.POST.get('anfitriona')


        plaza_dia = plazaAlmuerzo(m1 = m12a, r1 = r12, m2 = m14, r2 = r14, m3 = m15, r3 = r15, m4 = m16,
                                   r4 = r16, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

        mozo = request.POST.get('mozoplaza4')      
        m17 = request.POST.get('m17')
        r17 = request.POST.get('r17')
        m18 = request.POST.get('m18')
        r18 = request.POST.get('r18')
        m8 = request.POST.get('m8')
        r8 = request.POST.get('r8')
        m9 = request.POST.get('m9')
        r9 = request.POST.get('r9')
        m34 = request.POST.get('m34')
        r34 = request.POST.get('r34')
        total = request.POST.get('totalpz4')
        plaza = 'Plaza4'
        anfi = request.POST.get('anfitriona')


        plaza_dia = plazaAlmuerzo(m1 = m17, r1 = r17, m2 = m18, r2 = r18, m3 = m8, r3 = r8, m4 = m9,
                                   r4 = r9, m5 = m34, r5 = r34, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

        mozo = request.POST.get('mozoplaza5')      
        m26 = request.POST.get('m26')
        r26 = request.POST.get('r26')
        m19 = request.POST.get('m19')
        r19 = request.POST.get('r19')
        m20 = request.POST.get('m20')
        r20 = request.POST.get('r20')
        m21 = request.POST.get('m21')
        r21 = request.POST.get('r21')
        total = request.POST.get('totalpz5')
        plaza = 'Plaza5'
        anfi = request.POST.get('anfitriona')


        plaza_dia = plazaAlmuerzo(m1 = m26, r1 = r26, m2 = m19, r2 = r19, m3 = m20, r3 = r20, m4 = m21,
                                   r4 = r21, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

        mozo = request.POST.get('mozoplaza6')      
        m22 = request.POST.get('m22')
        r22 = request.POST.get('r22')
        m30 = request.POST.get('m30')
        r30 = request.POST.get('r30')
        m31 = request.POST.get('m31')
        r31 = request.POST.get('r31')
        m32 = request.POST.get('m32')
        r32 = request.POST.get('r32')
        total = request.POST.get('totalpz6')
        plaza = 'Plaza6'
        anfi = request.POST.get('anfitriona')


        plaza_dia = plazaAlmuerzo(m1 = m22, r1 = r22, m2 = m30, r2 = r30, m3 = m31, r3 = r31, m4 = m32,
                                   r4 = r32, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

        mozo = request.POST.get('mozoplaza7')      
        m27 = request.POST.get('m27')
        r27 = request.POST.get('r27')
        m28 = request.POST.get('m28')
        r28 = request.POST.get('r28')
        m29 = request.POST.get('m29')
        r29 = request.POST.get('r29')
        mb3 = request.POST.get('mb3')
        rb3 = request.POST.get('rb3')
        total = request.POST.get('totalpz7')
        plaza = 'Plaza7'
        anfi = request.POST.get('anfitriona')


        plaza_dia = plazaAlmuerzo(m1 = m27, r1 = r27, m2 = m28, r2 = r28, m3 = m29, r3 = r29, m4 = mb3,
                                   r4 = rb3, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

        mozo = request.POST.get('mozoplaza8')      
        m35 = request.POST.get('m35')
        r35 = request.POST.get('r35')
        m36 = request.POST.get('m36')
        r36 = request.POST.get('r36')
        m37 = request.POST.get('m37')
        r37 = request.POST.get('r37')
        m38 = request.POST.get('m38')
        r38 = request.POST.get('r38')
        m39 = request.POST.get('m39')
        r39 = request.POST.get('r39')
        total = request.POST.get('totalpz8')
        plaza = 'Plaza8'
        anfi = request.POST.get('anfitriona')


        plaza_dia = plazaAlmuerzo(m1 = m35, r1 = r35, m2 = m36, r2 = r36, m3 = m37, r3 = r37, m4 = m38,
                                   r4 = r38, m5 = m39, r5 = r39, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

        mozo = request.POST.get('mozoplaza9') + ' y ' +  request.POST.get('mozoplaza9b')    
        mjp = request.POST.get('mjp')
        rjp = request.POST.get('rjp')
        total = request.POST.get('totalpz9')
        plaza = 'Plaza9'
        anfi = request.POST.get('anfitriona')


        plaza_dia = plazaAlmuerzo(m1 = mjp, r1 = rjp, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

        mozo = request.POST.get('mozoplaza10') + ' y ' +  request.POST.get('mozoplaza10b')    
        mbelua = request.POST.get('mbelua')
        rbelua = request.POST.get('rbelua')
        total = request.POST.get('totalpz10')
        plaza = 'Plaza10'
        anfi = request.POST.get('anfitriona')


        plaza_dia = plazaAlmuerzo(m1 = mbelua, r1 = rbelua, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_dia.save()

def guardaPlazaCena(request):
    fecha_actual = datetime.now().date()
    hora_actual = datetime.now().strftime('%H:%M')

    if plazaCena.objects.filter(fecha_dia = fecha_actual).exists():
        return HttpResponse('La plaza ya ha sido guardada')


    if hora_actual < '23:30':
        return HttpResponse('No puede guardar la plaza hasta finalizar el turno')

    if request.method == 'POST':

        mozo = request.POST.get('mozoplaza1')      
        m1 = request.POST.get('m1c')
        r1 = request.POST.get('r1c')
        m2 = request.POST.get('m2c')
        r2 = request.POST.get('r2c')
        m3 = request.POST.get('m3c')
        r3 = request.POST.get('r3c')
        m6 = request.POST.get('m6c')
        r6 = request.POST.get('r6c')
        m6a = request.POST.get('m6Ac')
        r6a = request.POST.get('r6Ac')
        total = request.POST.get('totalpz1c')
        plaza = 'Plaza1'
        anfi = request.POST.get('anfitriona')

        plaza_cena = plazaCena(m1 = m1, r1 = r1, m2 = m2, r2 = r2, m3 = m3, r3 = r3,
                                   m4 = m6, r4 = r6, m5 = m6a, r5 = r6a, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()

        mozo = request.POST.get('mozoplaza2')      
        m4 = request.POST.get('m4c')
        r4 = request.POST.get('r4c')
        m5 = request.POST.get('m5c')
        r5 = request.POST.get('r5c')
        m10 = request.POST.get('m10c')
        r10 = request.POST.get('r10c')
        m11 = request.POST.get('m11c')
        r11 = request.POST.get('r11c')
        m12 = request.POST.get('m12c')
        r12 = request.POST.get('r12c')
        total = request.POST.get('totalpz2c')
        plaza = 'Plaza2'
        anfi = request.POST.get('anfitriona')


        plaza_cena = plazaCena(m1 = m4, r1 = r4, m2 = m5, r2 = r5, m3 = m10, r3 = r10, m4 = m11,
                                   r4 = r11, m5 = m12, r5 = r12, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()

        mozo = request.POST.get('mozoplaza3')      
        m12a = request.POST.get('m12Ac')
        r12 = request.POST.get('r12c')
        m14 = request.POST.get('m14c')
        r14 = request.POST.get('r14c')
        m15 = request.POST.get('m15c')
        r15 = request.POST.get('r15c')
        m16 = request.POST.get('m16c')
        r16 = request.POST.get('r16c')
        total = request.POST.get('totalpz3c')
        plaza = 'Plaza3'
        anfi = request.POST.get('anfitriona')


        plaza_cena = plazaCena(m1 = m12a, r1 = r12, m2 = m14, r2 = r14, m3 = m15, r3 = r15, m4 = m16,
                                   r4 = r16, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()

        mozo = request.POST.get('mozoplaza4')      
        m17 = request.POST.get('m17c')
        r17 = request.POST.get('r17c')
        m18 = request.POST.get('m18c')
        r18 = request.POST.get('r18c')
        m8 = request.POST.get('m8c')
        r8 = request.POST.get('r8c')
        m9 = request.POST.get('m9c')
        r9 = request.POST.get('r9c')
        m34 = request.POST.get('m34c')
        r34 = request.POST.get('r34c')
        total = request.POST.get('totalpz4c')
        plaza = 'Plaza4'
        anfi = request.POST.get('anfitriona')


        plaza_cena = plazaCena(m1 = m17, r1 = r17, m2 = m18, r2 = r18, m3 = m8, r3 = r8, m4 = m9,
                                   r4 = r9, m5 = m34, r5 = r34, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()

        mozo = request.POST.get('mozoplaza5')      
        m26 = request.POST.get('m26c')
        r26 = request.POST.get('r26c')
        m19 = request.POST.get('m19c')
        r19 = request.POST.get('r19c')
        m20 = request.POST.get('m20c')
        r20 = request.POST.get('r20c')
        m21 = request.POST.get('m21c')
        r21 = request.POST.get('r21c')
        total = request.POST.get('totalpz5c')
        plaza = 'Plaza5'
        anfi = request.POST.get('anfitriona')


        plaza_cena = plazaCena(m1 = m26, r1 = r26, m2 = m19, r2 = r19, m3 = m20, r3 = r20, m4 = m21,
                                   r4 = r21, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()

        mozo = request.POST.get('mozoplaza6')      
        m22 = request.POST.get('m22c')
        r22 = request.POST.get('r22c')
        m30 = request.POST.get('m30c')
        r30 = request.POST.get('r30c')
        m31 = request.POST.get('m31c')
        r31 = request.POST.get('r31c')
        m32 = request.POST.get('m32c')
        r32 = request.POST.get('r32c')
        total = request.POST.get('totalpz6c')
        plaza = 'Plaza6'
        anfi = request.POST.get('anfitriona')


        plaza_cena = plazaCena(m1 = m22, r1 = r22, m2 = m30, r2 = r30, m3 = m31, r3 = r31, m4 = m32,
                                   r4 = r32, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()

        mozo = request.POST.get('mozoplaza7')      
        m27 = request.POST.get('m27c')
        r27 = request.POST.get('r27c')
        m28 = request.POST.get('m28c')
        r28 = request.POST.get('r28c')
        m29 = request.POST.get('m29c')
        r29 = request.POST.get('r29c')
        mb3 = request.POST.get('mb3c')
        rb3 = request.POST.get('rb3c')
        total = request.POST.get('totalpz7c')
        plaza = 'Plaza7'
        anfi = request.POST.get('anfitriona')


        plaza_cena = plazaCena(m1 = m27, r1 = r27, m2 = m28, r2 = r28, m3 = m29, r3 = r29, m4 = mb3,
                                   r4 = rb3, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()

        mozo = request.POST.get('mozoplaza8')      
        m35 = request.POST.get('m35c')
        r35 = request.POST.get('r35c')
        m36 = request.POST.get('m36c')
        r36 = request.POST.get('r36c')
        m37 = request.POST.get('m37c')
        r37 = request.POST.get('r37c')
        m38 = request.POST.get('m38c')
        r38 = request.POST.get('r38c')
        m39 = request.POST.get('m39c')
        r39 = request.POST.get('r39c')
        total = request.POST.get('totalpz8c')
        plaza = 'Plaza8'
        anfi = request.POST.get('anfitriona')


        plaza_cena = plazaCena(m1 = m35, r1 = r35, m2 = m36, r2 = r36, m3 = m37, r3 = r37, m4 = m38,
                                   r4 = r38, m5 = m39, r5 = r39, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()

        mozo = request.POST.get('mozoplaza9') + ' y ' +  request.POST.get('mozoplaza9b')    
        mjp = request.POST.get('mjpc')
        rjp = request.POST.get('rjpc')
        total = request.POST.get('totalpz9c')
        plaza = 'Plaza9'
        anfi = request.POST.get('anfitriona')


        plaza_cena = plazaCena(m1 = mjp, r1 = rjp, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()

        mozo = request.POST.get('mozoplaza10') + ' y ' +  request.POST.get('mozoplaza10b')    
        mbelua = request.POST.get('mbeluac')
        rbelua = request.POST.get('rbeluac')
        total = request.POST.get('totalpz10c')
        plaza = 'Plaza10'
        anfi = request.POST.get('anfitriona')


        plaza_cena = plazaCena(m1 = mbelua, r1 = rbelua, total = total, plaza = plaza, mozo_nombre = mozo, nombre_anfitriona = anfi)
            
        plaza_cena.save()





 







    

