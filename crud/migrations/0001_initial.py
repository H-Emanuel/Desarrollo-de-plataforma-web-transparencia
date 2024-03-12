# Generated by Django 4.2.10 on 2024-03-01 15:34

import crud.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('fecha_i_t', models.DateTimeField()),
                ('fecha_i_au', models.DateTimeField()),
                ('N_transparencia', models.BigIntegerField()),
                ('dirigido', models.CharField(blank=True, default='', max_length=100)),
                ('region', models.CharField(blank=True, default='', max_length=100)),
                ('recepcion', models.CharField(blank=True, default='', max_length=100)),
                ('email', models.CharField(blank=True, default='', max_length=100)),
                ('solicitud_text', models.CharField(blank=True, default='', max_length=100)),
                ('observaciones', models.CharField(blank=True, default='', max_length=100)),
                ('archivo_adjunto', models.ImageField(blank=True, default='', null=True, upload_to=crud.models.content_file_name_adjunto)),
                ('soporte', models.CharField(blank=True, default='', max_length=100)),
                ('formato', models.CharField(blank=True, default='', max_length=100)),
                ('solicitante_inicio_seccion', models.CharField(blank=True, default='', max_length=100)),
                ('forma_de_recepccion', models.CharField(blank=True, default='', max_length=100)),
                ('otra_forma_De_entrega', models.CharField(blank=True, default='', max_length=100)),
                ('persona', models.CharField(blank=True, default='', max_length=100)),
                ('nombre_o_razon_social', models.CharField(blank=True, default='', max_length=100)),
                ('primer_apellido', models.CharField(blank=True, default='', max_length=100)),
                ('segundo_apellido', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'verbose_name': 'Solicitud',
                'verbose_name_plural': 'Solicitudes',
            },
        ),
        migrations.CreateModel(
            name='Respuesta_solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solicitud_text', models.CharField(blank=True, default='', max_length=100)),
                ('archivo_adjunto', models.ImageField(blank=True, default='', null=True, upload_to=crud.models.content_file_name_respuesta)),
                ('id_solicitud', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='crud.solicitud')),
            ],
            options={
                'verbose_name': 'Respuesta',
                'verbose_name_plural': 'Respuestas',
            },
        ),
    ]