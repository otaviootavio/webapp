# Generated by Django 4.1.1 on 2022-11-18 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_voobase_companhia_aerea_alter_voobase_destino_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vooreal',
            name='horario_real_chegada',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vooreal',
            name='horario_real_partida',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
