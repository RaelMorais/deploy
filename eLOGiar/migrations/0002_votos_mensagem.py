# Generated by Django 5.1.6 on 2025-02-19 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eLOGiar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='votos',
            name='mensagem',
            field=models.CharField(default='Texto por defecto', max_length=255),
        ),
    ]
