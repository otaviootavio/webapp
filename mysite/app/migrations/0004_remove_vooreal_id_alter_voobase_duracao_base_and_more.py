# Generated by Django 4.1.1 on 2022-11-18 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_voobase_horario_partida_base_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vooreal',
            name='id',
        ),
        migrations.AlterField(
            model_name='voobase',
            name='duracao_base',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='voobase',
            name='horario_partida_base',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='vooreal',
            name='voo_base',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.voobase'),
        ),
    ]
