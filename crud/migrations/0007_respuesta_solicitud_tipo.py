# Generated by Django 3.2.15 on 2024-06-25 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0006_auto_20240502_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta_solicitud',
            name='tipo',
            field=models.CharField(choices=[('A', 'Amparo'), ('R', 'Respuesta')], default='R', max_length=1),
        ),
    ]