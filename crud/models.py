from django.db import models
import os
from django.contrib.auth.models import User

# Create your models here.
RECEPCION_CHOICES = [
    ('CORREO ELECTRONICOS', 'CORREO ELECTRONICOS'),
    ('PAPEL', 'PAPEL'),
]

RESPUESTA_PERSONA_CHOICES = [
    ('NATURAL', 'NATURAL'),
    ('EMPRESA', 'EMPRESA'),
]

DEPARTAMENTO_CHOICES = [
    ('Departamento de Asesoría Urbana ', 'Departamento de Asesoría Urbana'),
    ('Departamento de Presupuesto Municipal y Control Financiero de Proyectos', 'Departamento de Presupuesto Municipal y Control Financiero de Proyectos'),
    ('Departamento de Planificación ', 'Departamento de Planificación'),
    ('Departamento de Estudios y Pre Inversión ', 'Departamento de Estudios y Pre Inversión'),
    ('Departamento de Sistema de Información Geográfica ', 'Departamento de Sistema de Información Geográfica'),
    ('ADMIN', 'ADMIN'),
]


DEPARTAMENTO_CHOICES_2 = [
    ('Departamento de Asesoría Urbana ', 'Departamento de Asesoría Urbana'),
    ('Departamento de Presupuesto Municipal y Control Financiero de Proyectos', 'Departamento de Presupuesto Municipal y Control Financiero de Proyectos'),
    ('Departamento de Planificación ', 'Departamento de Planificación'),
    ('Departamento de Estudios y Pre Inversión ', 'Departamento de Estudios y Pre Inversión'),
    ('Departamento de Sistema de Información Geográfica ', 'Departamento de Sistema de Información Geográfica'),
]

def content_file_name_adjunto(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('p', ext)
    return os.path.join('assets_adjunto', filename)


class Solicitud(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    fecha_i_t = models.DateField()
    fecha_i_au = models.DateField()
    N_transparencia = models.CharField(max_length=100, blank=True, default='')

    # PARTE 2

    dirigido = models.CharField(max_length=100, blank=True, default='Municipalidad de Valparaíso')
    region = models.CharField(max_length=100, blank=True, default='Región de Valparaiso')
    recepcion = models.CharField(max_length=50, blank=True, default='',choices=RECEPCION_CHOICES)

    email = models.CharField(max_length=150, blank=True, default='')
    solicitud_text = models.TextField(blank=True, default='')
    observaciones = models.TextField(blank=True, default='')
    archivo_adjunto = models.ImageField(upload_to=content_file_name_adjunto, blank=True, default='',null=True)

    soporte = models.CharField(max_length=150, blank=True, default='')
    formato = models.CharField(max_length=150, blank=True, default='')

    solicitante_inicio_seccion = models.BooleanField(default=False)
    forma_de_recepccion = models.CharField(max_length=150, blank=True,choices=RECEPCION_CHOICES, default='')
    otra_forma_De_entrega = models.CharField(max_length=150, blank=True, default='')

   # PARTE 3 
    
    persona = models.CharField(max_length=50, blank=True, default='',choices=RESPUESTA_PERSONA_CHOICES)
    nombre_o_razon_social = models.CharField(max_length=150, blank=True, default='')
    primer_apellido = models.CharField(max_length=100, blank=True, default='')
    segundo_apellido = models.CharField(max_length=100, blank=True, default='')

    # PARTE 4 - ADMIN EXCLUSIVOS

    estado = models.CharField(max_length=100, blank=True, default='Sin responder')
    fecha_limite = models.DateField()
    Departamento_admin = models.CharField(max_length=150, blank=True, default='',choices=DEPARTAMENTO_CHOICES_2, null=True) 


    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"


def content_file_name_respuesta(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('p', ext)
    folder = "assets_respuesta/" + str(instance.id_solicitud.id)
    return os.path.join(folder, filename)


class Respuesta_solicitud(models.Model): 
    id_solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    respuesta = models.TextField(blank=True, default='')
    archivo_adjunto = models.ImageField(upload_to=content_file_name_respuesta, blank=True, default='', null=True)
    archivo_adjunto_2 = models.ImageField(upload_to=content_file_name_respuesta, blank=True, default='', null=True)
    archivo_adjunto_3 = models.ImageField(upload_to=content_file_name_respuesta, blank=True, default='', null=True)
    fecha_daj = models.DateField(blank=True)

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"

class Departamento(models.Model): 
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True )
    nombre_departamento = models.CharField(max_length=150, blank=True, default='',choices=DEPARTAMENTO_CHOICES)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamento"
