# Generated by Django 4.2.10 on 2024-05-13 21:33

from django.db import migrations, models
import pdf_link.models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_link', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf_link',
            name='archivo_adjunto',
            field=models.ImageField(blank=True, default='', null=True, upload_to=pdf_link.models.content_file_name_adjunto),
        ),
    ]
