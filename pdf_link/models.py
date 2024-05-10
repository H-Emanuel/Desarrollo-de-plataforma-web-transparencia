from django.db import models
import os


# aqui se guarda los pdf
def content_file_name_adjunto(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('p', ext)
    return os.path.join('asset_pdf_link', filename)

# Create your models here.
class Pdf_link(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    id_excel = models.IntegerField()
    fecha_I = models.DateField()
    fecha_E = models.DateField()
    nombre = models.CharField(max_length=100, blank=True, default='')
    archivo_adjunto = models.ImageField(upload_to=content_file_name_adjunto, blank=True, default='',null=True)


    class Meta:
        verbose_name = "Pdf_link"
        verbose_name_plural = "Pdf_links"
