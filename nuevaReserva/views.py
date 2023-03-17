from django.shortcuts import render, HttpResponse, redirect
from .forms import nuevaReservaFoms, editReservaFoms
from django.contrib import messages
from .models import nuevaReserva
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
    completado = nuevaReserva.objects.filter(estado_id__gt= 1).order_by('-fechaReserva')
    cuenta_completado = nuevaReserva.objects.filter(estado_id = 2).count()
    return render(request, 'listadoHistorico.html', {"listaCompletado": completado, "totalCompletado":cuenta_completado})
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

def guardarMesa(request, id):
    
    if request.method == 'POST':
        mesa = request.POST.get('mesa')
        cambiaMesa = nuevaReserva.objects.get(id = id)
        cambiaMesa.mesa = mesa
        cambiaMesa.save()

        return redirect('delDia')

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

 







    

