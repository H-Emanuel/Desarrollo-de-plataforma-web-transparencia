# Generated by Django 3.2.15 on 2024-06-25 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0007_respuesta_solicitud_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta_solicitud',
            name='id_solicitud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud.solicitud'),
        ),
    ]