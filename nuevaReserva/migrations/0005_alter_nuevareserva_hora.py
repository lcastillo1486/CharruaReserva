# Generated by Django 4.1.5 on 2023-02-20 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevaReserva', '0004_mesa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nuevareserva',
            name='hora',
            field=models.TimeField(help_text='Enter field documentation'),
        ),
    ]
