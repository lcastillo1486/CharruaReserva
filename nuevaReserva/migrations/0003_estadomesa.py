# Generated by Django 4.1.5 on 2023-02-20 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevaReserva', '0002_nuevareserva'),
    ]

    operations = [
        migrations.CreateModel(
            name='estadoMesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=15)),
            ],
        ),
    ]
