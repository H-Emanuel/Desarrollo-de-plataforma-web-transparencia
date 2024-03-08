# Generated by Django 4.2.10 on 2024-03-06 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respuesta_solicitud',
            name='solicitud_text',
        ),
        migrations.AddField(
            model_name='respuesta_solicitud',
            name='respuesta',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='N_transparencia',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='dirigido',
            field=models.CharField(blank=True, default='Municipalidad de Valparaíso', max_length=100),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='email',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='forma_de_recepccion',
            field=models.CharField(blank=True, choices=[('CORREO ELECTRONICOS', 'CORREO ELECTRONICOS'), ('PAPEL', 'PAPEL')], default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='formato',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='nombre_o_razon_social',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='observaciones',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='otra_forma_De_entrega',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='persona',
            field=models.CharField(blank=True, choices=[('NATURAL', 'NATURAL'), ('EMPRESA', 'EMPRESA')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='recepcion',
            field=models.CharField(blank=True, choices=[('CORREO ELECTRONICOS', 'CORREO ELECTRONICOS'), ('PAPEL', 'PAPEL')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='region',
            field=models.CharField(blank=True, default='Región de Valparaiso', max_length=100),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='solicitante_inicio_seccion',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='solicitud_text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='soporte',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
