from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
from django.http import JsonResponse


@login_required(login_url='/login/')
def home(request):
    OPTIONS = {
        # 'PLAN_CERRO_POBLACION': PLAN_CERRO_POBLACION,
        'RECEPCION_CHOICES': RECEPCION_CHOICES,
        'RESPUESTA_PERSONA_CHOICES': RESPUESTA_PERSONA_CHOICES,
        }
    data = {'OPTIONS': OPTIONS,}
    if request.method == "POST":
            fecha_ingreso_t = datetime.strptime(request.POST['Fecha_ingreso_t'], '%Y-%m-%d').date()
            fecha_ingreso_au = datetime.strptime(request.POST['Fecha_ingreso_AU'], '%Y-%m-%d').date()

            N_transparencia = request.POST['N_transparencia']

            dirigido = "Municipalidad de Valparaíso"
            region = "Región de Valparaiso"
            recepcion = request.POST['recepcion'],
            email = request.POST['e_email']
            solicitud_text = request.POST['solicitud_text']
            observaciones = request.POST['observaciones']

            try: 
                archivo_adjunto = request.FILES['archivo_adjunto']
            except:
                archivo_adjunto = ""

            soporte = request.POST['soporte']
            formato = request.POST['formato']

            if request.POST['solicitante_inicio_seccion']  =="Si":
                solicitante_inicio_seccion = True 
            else: 
                solicitante_inicio_seccion = False 

            
            forma_de_recepccion = request.POST['forma_de_recepccion']
            otra_forma_De_entrega = request.POST['otra_forma_De_entrega']

            
            persona = request.POST['persona']
            nombre_o_razon_social = request.POST['nombre_o_razon_social']
            primer_apellido = request.POST['primer_apellido']
            segundo_apellido = request.POST['segundo_apellido']

            Solicitud.objects.create(
                  
                fecha_i_t = fecha_ingreso_t,
                fecha_i_au = fecha_ingreso_au,
                N_transparencia = N_transparencia,

                dirigido = dirigido,
                region =region,
                recepcion =recepcion,
                email = email,
                solicitud_text = solicitud_text,
                observaciones = observaciones,
                archivo_adjunto = archivo_adjunto,

                soporte = soporte,
                formato = formato,

                solicitante_inicio_seccion = solicitante_inicio_seccion, # cambio de verdadero o falso
                
                forma_de_recepccion = forma_de_recepccion,
                otra_forma_De_entrega = otra_forma_De_entrega,

            # PARTE 3 
                
                persona = persona,
                nombre_o_razon_social = nombre_o_razon_social,
                primer_apellido = primer_apellido,
                segundo_apellido = segundo_apellido,

            )
            return redirect('home')

    return render(request, 'home.html',data)

def read(request):
    Solicitud_read = Solicitud.objects.all()
    respuesta_dict = {}  # Diccionario para almacenar las respuestas

    # Iterar sobre cada objeto Solicitud en el queryset
    for solicitud in Solicitud_read:
        try:
            # Intentar obtener la respuesta asociada a esta Solicitud
            respuesta = Respuesta_solicitud.objects.get(id_solicitud=solicitud)
            respuesta_dict[solicitud.id] = respuesta  # Agregar la respuesta al diccionario
        except Respuesta_solicitud.DoesNotExist:
            # Si no hay respuesta asociada, asignar None
            respuesta_dict[solicitud.id] = None

    # Combinar los datos de Solicitud_read y respuesta_dict en una lista de tuplas
    solicitud_respuesta_list = [(solicitud, respuesta_dict.get(solicitud.id)) for solicitud in Solicitud_read]

    data = {
        'solicitud_respuesta_list': solicitud_respuesta_list,  # Pasar la lista combinada al contexto
    }

    return render(request, 'read.html', data)


    
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

def vista_previa_respuesta(request, id):
    respuesta = Respuesta_solicitud.objects.get(id=id)

    data = {

        'respuesta': respuesta.respuesta,
        'fecha_daj': respuesta.fecha_daj,
        'archivo_adjunto_url': respuesta.archivo_adjunto.url if respuesta.archivo_adjunto else None,

    }
    return JsonResponse(data)

def respuesta(request, id=0):
    if request.method == 'POST':
        fecha_daj = request.POST['Fecha_ingreso_DAJ']

        respuesta_text = request.POST['respuesta']
        try: 
            archivo_adjunto = request.FILES['archivo_adjunto']
        except:
            archivo_adjunto = None  # Utiliza None en lugar de una cadena vacía

        # Obtener la instancia de Solicitud correspondiente al ID
        solicitud = Solicitud.objects.get(id=id)

        # Crear una nueva instancia de Respuesta_solicitud y asignar la solicitud
        Respuesta_solicitud.objects.create(
            fecha_daj = fecha_daj,
            id_solicitud=solicitud,  # Asignar la instancia de Solicitud
            respuesta=respuesta_text,
            archivo_adjunto=archivo_adjunto,
        )

        # Actualizar el estado de la solicitud a "RESPONDIDA"
        solicitud.estado = "Respondida"
        solicitud.save()

        return redirect('read')
    
    return render(request, 'crud_respuesta.html',)