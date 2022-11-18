from datetime import datetime, timedelta, time
from math import floor
from django.db import models
from django.forms import ModelForm

COMPANHIAS_AEREAS = (
     ('AZU','Azul'),
     ('GLO','Gol'),
     ('TAM','LATAM'),
    )

DIAS_SEMANA = (
        ('SEG','Segunda'),
        ('TER','Terca'),
        ('QUA','Quarta'),
        ('QUI','Quinta'),
        ('SEX','Sexta'),
        ('SAB','Sabado'),
        ('DOM','Domingo')
    )

ESTADOS_VOO = (
     ('AGD','Agendado'),
     ('EMB','Embarcando'),
     ('CAN','Cancelado'),
     ('PRG','Programado'),
     ('TAX','Taxiando'),
     ('PRT','Pronto'),
     ('AUT','Autorizado'),
     ('EMV','Em voo'),
     ('ATE','Aterrisado'),
    )

ESTADOS = (
('AC','Acre'),
('AL','Alagoas'),
('AP','Amapá'),
('AM','Amazonas'),
('BA','Bahia'),
('CE','Ceará'),
('DF','Distrito Federal'),
('ES','Espírito Santo'),
('GO', 'Goiás'),
('MA', 'Maranhão'),
('MT', 'Mato Grosso'),
('MS', 'Mato Grosso do Sul'),
('MG', 'Minas Gerais'),
('PA','Pará'),
('PB', 'Paraíba'),
('PR','Paraná'),
('PE','Pernambuco'),
('PI','Piauí'),
('RJ', 'Rio de Janeiro'),
('RN', 'Rio Grande do Norte'),
('RS', 'Rio Grande do Sul'),
('RO', 'Rondônia'),
('RR', 'Roraima'),
('SC','Santa Catarina'),
('SP','São Paulo'),
('SE','Sergipe'),
('TO','Tocantins'),
)

class VooBase(models.Model):
    codigo_voo = models.CharField(max_length=200, null=False, blank = False)
    companhia_aerea = models.CharField(max_length=200,choices=COMPANHIAS_AEREAS ,null=False)
    dia_da_semana = models.CharField(max_length = 3, choices = DIAS_SEMANA, null = False)
    horario_partida_base = models.TimeField(null=False)
    duracao_base = models.TimeField(null=False)
    origem = models.CharField(max_length=200,choices=ESTADOS, null=False)
    destino = models.CharField(max_length=200,choices=ESTADOS, null=False)

    def get_horario_chegada(this):
        hour_duracao = floor(this.duracao_base / 3600)
        minute_duracao = floor((this.duracao_base - hour_duracao*3600) / 60 )
        seconds_duracao = this.duracao_base - hour_duracao*3600 - minute_duracao*60
        
        hour_base = this.horario_partida_base.hour
        minute_base = this.horario_partida_base.minute
        second_base = this.horario_partida_base.second
        
        seconds_total = second_base + seconds_duracao
        hour_total = hour_base + hour_duracao
        minute_total = minute_base + minute_duracao
        
        if(seconds_total > 60 ):
            minutes_total = minutes_total + floor(seconds_total/60)
            seconds_total = seconds_total % 60
        
        if(minute_total > 60 ):
            hour_total = hour_total + floor(minute_total/60)
            minute_total = minute_total % 60
        
        time_total = time(hour = hour_total, minute = minute_total, second = seconds_total)

        return time_total

    class Meta:
        db_table = 'voo_base'

class VooReal(models.Model):    
    voo_base = models.OneToOneField(VooBase, on_delete=models.CASCADE, blank=True, primary_key=True)
    data_voo = models.DateField()
    estado_voo = models.CharField(max_length = 3, choices = ESTADOS_VOO)
    horario_real_chegada = models.TimeField(auto_now=False, auto_now_add=False, null=True,blank=True)
    horario_real_partida = models.TimeField(auto_now=False, auto_now_add=False, null=True,blank=True)
    
    class Meta:
        db_table = 'voo_real'