# Generated by Django 4.1.5 on 2023-03-20 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevaReserva', '0012_nuevareserva_mesa_asignadaa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nuevareserva',
            name='emailr',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
