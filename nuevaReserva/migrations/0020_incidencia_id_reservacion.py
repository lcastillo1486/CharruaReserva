# Generated by Django 4.1.5 on 2023-08-11 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevaReserva', '0019_incidencialog'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidencia',
            name='id_reservacion',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
