from django.db import models
import os
# Create your models here.
def content_file_name_adjunto(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('p', ext)
    folder = "assets_adjunto/" + str(instance.id.id)
    return os.path.join(folder, filename)

class Solicitud(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)    
    # PARTE 1
    fecha_i_t = models.DateTimeField()
    fecha_i_au = models.DateTimeField()
    N_transparencia = models.BigIntegerField()

    # PARTE 2

    dirigido = models.CharField(max_length=100, blank=True, default='')
    region = models.CharField(max_length=100, blank=True, default='')
    recepcion = models.CharField(max_length=100, blank=True, default='')

    email = models.CharField(max_length=100, blank=True, default='')
    solicitud_text = models.CharField(max_length=100, blank=True, default='')
    observaciones = models.CharField(max_length=100, blank=True, default='')
    archivo_adjunto = models.ImageField(upload_to=content_file_name_adjunto, blank=True, default='',null=True)

    soporte = models.CharField(max_length=100, blank=True, default='')
    formato = models.CharField(max_length=100, blank=True, default='')

    solicitante_inicio_seccion = models.CharField(max_length=100, blank=True, default='')
    forma_de_recepccion = models.CharField(max_length=100, blank=True, default='')
    otra_forma_De_entrega = models.CharField(max_length=100, blank=True, default='')

   # PARTE 3 
    
    persona = models.CharField(max_length=100, blank=True, default='')
    nombre_o_razon_social = models.CharField(max_length=100, blank=True, default='')
    primer_apellido = models.CharField(max_length=100, blank=True, default='')
    segundo_apellido = models.CharField(max_length=100, blank=True, default='')


    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"


def content_file_name_respuesta(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('p', ext)
    folder = "assets_respuesta/" + str(instance.id.id)
    return os.path.join(folder, filename)

class Respuesta_solicitud(models.Model):
    id_solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    # PARTE 1
    solicitud_text = models.CharField(max_length=100, blank=True, default='')
    archivo_adjunto = models.ImageField(upload_to=content_file_name_respuesta, blank=True, default='',null=True)

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"