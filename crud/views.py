from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import *
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from PyPDF2 import PdfMerger, PdfReader  
from django.core.files.base import ContentFile
import io


@login_required(login_url='/login/')
def home(request):
    user = request.user
    departamento_usuario = Departamento.objects.filter(id_usuario=user).first()

    OPTIONS = {
        'RECEPCION_CHOICES': RECEPCION_CHOICES,
        'RESPUESTA_PERSONA_CHOICES': RESPUESTA_PERSONA_CHOICES,
        'DEPARTAMENTO_CHOICES': DEPARTAMENTO_CHOICES_2,        
    }
    
    data = {'OPTIONS': OPTIONS, 'departamento': departamento_usuario}

    if request.method == "POST":
        fecha_ingreso_t = datetime.strptime(request.POST['Fecha_ingreso_t'], '%Y-%m-%d').date()
        fecha_ingreso_au = datetime.strptime(request.POST['Fecha_ingreso_AU'], '%Y-%m-%d').date()
        N_transparencia = request.POST['N_transparencia']
        dirigido = "Municipalidad de Valparaíso"
        region = "Región de Valparaiso"
        recepciones = request.POST['recepcion']
        email = request.POST['e_email']
        solicitud_text = request.POST['solicitud_text']
        observaciones = request.POST['observaciones']

        try: 
            archivo_adjunto = request.FILES['archivo_adjunto']
        except:
            archivo_adjunto = ""

        soporte = request.POST['soporte']
        formato = request.POST['formato']
        solicitante_inicio_seccion = request.POST['solicitante_inicio_seccion'] == "Si"
        forma_de_recepccion = request.POST['forma_de_recepccion']
        otra_forma_De_entrega = request.POST['otra_forma_De_entrega']
        persona = request.POST['persona']
        nombre_o_razon_social = request.POST['nombre_o_razon_social']
        primer_apellido = request.POST['primer_apellido']
        segundo_apellido = request.POST['segundo_apellido']
        fecha_limite = calcular_fecha_limite(fecha_ingreso_t)

        if departamento_usuario.nombre_departamento == "ADMIN":
            Departamento_admin = request.POST['departamento_admin']
        else:
            Departamento_admin = ""

        # Crear la solicitud
        Solicitud.objects.create(
            fecha_i_t=fecha_ingreso_t,
            fecha_i_au=fecha_ingreso_au,
            N_transparencia=N_transparencia,
            dirigido=dirigido,
            region=region,
            recepcion=recepciones,
            email=email,
            solicitud_text=solicitud_text,
            observaciones=observaciones,
            archivo_adjunto=archivo_adjunto,
            soporte=soporte,
            formato=formato,
            solicitante_inicio_seccion=solicitante_inicio_seccion,
            forma_de_recepccion=forma_de_recepccion,
            otra_forma_De_entrega=otra_forma_De_entrega,
            persona=persona,
            nombre_o_razon_social=nombre_o_razon_social,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            id_usuario=request.user,
            fecha_limite=fecha_limite,
            Departamento_admin=Departamento_admin
        )
        return redirect('home')

    return render(request, 'home.html', data)


@login_required  # Asegura que el usuario esté autenticado para acceder a esta vista
def read(request):
    user = request.user
    departamento_usuario = Departamento.objects.filter(id_usuario=user).first()

    if departamento_usuario and departamento_usuario.nombre_departamento == 'ADMIN':
        # Si el usuario es del departamento 'ADMIN', mostrar todas las solicitudes y respuestas
        solicitud_respuesta_list = []
        for solicitud in Solicitud.objects.all():
            respuesta = Respuesta_solicitud.objects.filter(id_solicitud=solicitud).first()
            departamento_origen = Departamento.objects.filter(id_usuario=solicitud.id_usuario).first()
            solicitud_respuesta_list.append((solicitud, respuesta, departamento_origen))

    else:
        # Si el usuario no es del departamento 'ADMIN', filtrar por usuario
        solicitud_respuesta_list = []
        for solicitud in Solicitud.objects.filter(id_usuario=user):
            try:
                # Intentar obtener la respuesta asociada a esta Solicitud
                respuesta = Respuesta_solicitud.objects.get(id_solicitud=solicitud)
            except Respuesta_solicitud.DoesNotExist:
                # Si no hay respuesta asociada, asignar None
                respuesta = None
            departamento_origen = Departamento.objects.filter(id_usuario=solicitud.id_usuario).first()
            solicitud_respuesta_list.append((solicitud, respuesta, departamento_origen))

    data = {
        'solicitud_respuesta_list': solicitud_respuesta_list,
        'departamento': departamento_usuario,
    }

    return render(request, 'read.html', data)



def calcular_fecha_limite(fecha_ingreso):
    # Contador para llevar la cuenta de los días hábiles
    dias_habiles = 0
    fecha_actual = fecha_ingreso  # Comenzar desde la fecha de ingreso

    # Bucle para encontrar la fecha límite
    while dias_habiles < 13:
        # Si es sábado o domingo, no se cuentan como días hábiles
        if fecha_actual.weekday() not in [5, 6]:
            dias_habiles += 1
        fecha_actual += timedelta(days=1)

    return fecha_actual - timedelta(days=1)  # Restar un día para incluir la fecha de ingreso

def calcular_prorroga(fecha_limite, dias_prorroga):
    dias_habiles = 0
    fecha_actual = fecha_limite  # Comenzar desde la fecha límite

    while dias_habiles < dias_prorroga:
        if fecha_actual.weekday() not in [5, 6]:
            dias_habiles += 1
        fecha_actual += timedelta(days=1)

    return fecha_actual - timedelta(days=1)  # Restar un día para incluir la fecha límite

def prorroga(request, id):
    if request.method == "POST":
        solicitud = get_object_or_404(Solicitud, id=id)
        
        if solicitud.prorroga_realizada:
            return redirect('read')  # Ya se ha realizado una prórroga

        dias_prorroga = int(request.POST['dias_prorroga'])
        if dias_prorroga > 10:
            dias_prorroga = 10
        
        nueva_fecha_limite = calcular_prorroga(solicitud.fecha_limite, dias_prorroga)
        solicitud.fecha_limite = nueva_fecha_limite
        solicitud.prorroga_realizada = True
        solicitud.save()
        return redirect('read')
    else:
        return redirect('read')

@login_required
def vista_previa_solicitud(request, id):
    solicitud = Solicitud.objects.get(id=id)

    data = {
        'fecha_i_t': solicitud.fecha_i_t.strftime('%Y-%m-%d'),
        'fecha_i_au': solicitud.fecha_i_au.strftime('%Y-%m-%d'),
        'N_transparencia': solicitud.N_transparencia,
        'dirigido': solicitud.dirigido,
        'region': solicitud.region,
        'recepcion': solicitud.recepcion,
        'email': solicitud.email,
        'solicitud_text': solicitud.solicitud_text,
        'observaciones': solicitud.observaciones,
        'archivo_adjunto_url': solicitud.archivo_adjunto.url if solicitud.archivo_adjunto else None,
        'soporte': solicitud.soporte,
        'formato': solicitud.formato,
        'solicitante_inicio_seccion': solicitud.solicitante_inicio_seccion,
        'forma_de_recepccion': solicitud.forma_de_recepccion,
        'otra_forma_De_entrega': solicitud.otra_forma_De_entrega,
        'persona': solicitud.persona,
        'nombre_o_razon_social': solicitud.nombre_o_razon_social,
        'primer_apellido': solicitud.primer_apellido,
        'segundo_apellido': solicitud.segundo_apellido,
    }
    return JsonResponse(data)

@login_required
def vista_previa_respuesta(request, id):
    tipo = request.GET.get('tipo')
    if tipo == 'A':
        respuestas = Respuesta_solicitud.objects.filter(id_solicitud=id, tipo=tipo).order_by('fecha_daj')
        data = {
            'respuestas': [
                {
                    'respuesta': respuesta.respuesta,
                    'fecha_daj': respuesta.fecha_daj,
                    'archivo_adjunto_url': respuesta.archivo_adjunto.url if respuesta.archivo_adjunto else None,
                    'archivo_adjunto_url_2': respuesta.archivo_adjunto_2.url if respuesta.archivo_adjunto_2 else None,
                    'archivo_adjunto_url_3': respuesta.archivo_adjunto_3.url if respuesta.archivo_adjunto_3 else None,
                } for respuesta in respuestas
            ]
        }
    else:
        respuesta = Respuesta_solicitud.objects.filter(id_solicitud=id, tipo=tipo).last()
        if respuesta:
            data = {
                'respuesta': respuesta.respuesta,
                'fecha_daj': respuesta.fecha_daj,
                'archivo_adjunto_url': respuesta.archivo_adjunto.url if respuesta.archivo_adjunto else None,
                'archivo_adjunto_url_2': respuesta.archivo_adjunto_2.url if respuesta.archivo_adjunto_2 else None,
                'archivo_adjunto_url_3': respuesta.archivo_adjunto_3.url if respuesta.archivo_adjunto_3 else None,
            }
        else:
            data = {}
    
    return JsonResponse(data)


@login_required
def respuesta(request, id=0):
    solicitud = get_object_or_404(Solicitud, id=id)
    Titulo = "CREACIÓN"

    # Obtener el tipo de respuesta desde los parámetros de la URL o establecer un valor por defecto
    tipo_respuesta = request.GET.get('tipo', 'R')

    data = {
        'solicitud': solicitud,
        'Titulo': Titulo,
        'tipo': tipo_respuesta  # Pasamos el tipo de respuesta al contexto
    }

    if request.method == 'POST':
        fecha_daj = request.POST['Fecha_ingreso_DAJ']
        respuesta_text = request.POST['respuesta']

        try:
            archivos_adjuntos_1 = request.FILES.getlist('archivo_adjunto')
        except KeyError:
            archivos_adjuntos_1 = None

        try:
            archivos_adjuntos_2 = request.FILES.getlist('archivo_adjunto_2')
        except KeyError:
            archivos_adjuntos_2 = None

        try:
            archivos_adjuntos_3 = request.FILES.getlist('archivo_adjunto_3')
        except KeyError:
            archivos_adjuntos_3 = None

        pdf_comprimido_1 = procesar_archivos_adjuntos(archivos_adjuntos_1)
        pdf_comprimido_3 = procesar_archivos_adjuntos(archivos_adjuntos_3)


        # Crear la respuesta de la solicitud
        Respuesta_solicitud.objects.create(
            fecha_daj=fecha_daj,
            id_solicitud=solicitud,
            respuesta=respuesta_text,
            archivo_adjunto=pdf_comprimido_1,
            archivo_adjunto_2=archivos_adjuntos_2,
            archivo_adjunto_3=pdf_comprimido_3,
            tipo=tipo_respuesta
        )

        # Actualizar el estado de la solicitud a "Respondida"
        solicitud.estado = "Respondida"
        solicitud.save()

        return redirect('read')
    
    return render(request, 'crud_respuesta.html', data)

def procesar_archivos_adjuntos(archivos_adjuntos):
    pdf_merger = PdfMerger()
    any_pdf_added = False

    for archivo in archivos_adjuntos:
        if archivo.content_type == 'application/pdf':
            pdf_merger.append(archivo)
            any_pdf_added = True
        else:
            # Manejar el caso en el que un archivo no sea PDF (opcional)
            pass

    if any_pdf_added:
        output_pdf = io.BytesIO()
        pdf_merger.write(output_pdf)
        pdf_merger.close()
        output_pdf.seek(0)
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_comprimido = f"archivo_comprimido_{timestamp}.pdf"
        pdf_comprimido = ContentFile(output_pdf.read(), name=nombre_archivo_comprimido)
    else:
        pdf_comprimido = None

    return pdf_comprimido


@login_required
def respuesta_edit(request, id=0):
    Titulo = "EDICION"
    respuesta = get_object_or_404(Respuesta_solicitud, id=id)

    data = {
        'Respuesta': respuesta,
        'Titulo': Titulo
    }

    if request.method == 'POST':
        fecha_daj = request.POST['Fecha_ingreso_DAJ']
        respuesta_text = request.POST['respuesta']

        try:
            archivos_adjuntos_1 = request.FILES.getlist('archivo_adjunto')
        except KeyError:
            archivos_adjuntos_1 = None

        try:
            archivos_adjuntos_2 = request.FILES.getlist('archivo_adjunto_2')
        except KeyError:
            archivos_adjuntos_2 = None

        try:
            archivos_adjuntos_3 = request.FILES.getlist('archivo_adjunto_3')
        except KeyError:
            archivos_adjuntos_3 = None

        # pdf_comprimido_1 = procesar_archivos_adjuntos(archivos_adjuntos_1)
        # pdf_comprimido_2 = procesar_archivos_adjuntos(archivos_adjuntos_2)
        # pdf_comprimido_3 = procesar_archivos_adjuntos(archivos_adjuntos_3)

        # Combinar archivos nuevos con los antiguos
        archivo_adjunto_combinado = combinar_archivos_adjuntos(archivos_adjuntos_1, respuesta.archivo_adjunto)
        archivo_adjunto_3_combinado = combinar_archivos_adjuntos(archivos_adjuntos_3, respuesta.archivo_adjunto_3)

        # Actualizar la respuesta de la solicitud
        respuesta.fecha_daj = fecha_daj
        respuesta.respuesta = respuesta_text
        respuesta.archivo_adjunto = archivo_adjunto_combinado
        respuesta.archivo_adjunto_2 = archivos_adjuntos_2
        respuesta.archivo_adjunto_3 = archivo_adjunto_3_combinado
        respuesta.save()

        return redirect('read')

    return render(request, 'crud_respuesta.html', data)



def combinar_archivos_adjuntos(archivos_nuevos, archivo_viejo):
    pdf_merger = PdfMerger()

    # Función para cargar archivo PDF como PdfReader
    def cargar_pdf_como_reader(archivo):
        try:
            reader = PdfReader(archivo)
            if reader.is_encrypted:
                raise ValueError("El archivo PDF está encriptado y no se puede combinar.")
            return reader
        except Exception as e:
            raise ValueError(f"No se pudo cargar el archivo PDF: {e}")

    # Combinar archivos nuevos si existen
    for archivo_nuevo in archivos_nuevos:
        if archivo_nuevo:
            pdf_reader = cargar_pdf_como_reader(archivo_nuevo)
            pdf_merger.append(pdf_reader)

    # Combinar archivo viejo si existe
    if archivo_viejo:
        pdf_reader_viejo = cargar_pdf_como_reader(archivo_viejo)
        pdf_merger.append(pdf_reader_viejo)

    # Crear archivo PDF combinado en memoria
    output_pdf = io.BytesIO()
    pdf_merger.write(output_pdf)
    pdf_merger.close()

    # Resetear el puntero al principio del archivo en memoria
    output_pdf.seek(0)

    # Generar un nombre único para el archivo usando un timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_comprimido = f"archivo_comprimido_{timestamp}.pdf"

    # Crear un ContentFile para guardar en el modelo
    pdf_comprimido = ContentFile(output_pdf.read(), name=nombre_archivo_comprimido)

    return pdf_comprimido
