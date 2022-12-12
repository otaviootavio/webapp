from datetime import time
from django.core.exceptions import ValidationError
from math import floor
from django.db import models
from enum import Enum
import datetime

class Group(Enum):
    gerentes = "gerentes"
    torres = "torres"
    pilotos = "pilotos"
    operadores = "operadores"
    funcionarios = "funcionarios"
    
COMPANHIAS_AEREAS = (
     ('AZU','Azul'),
     ('GLO','Gol'),
     ('TAM','LATAM'),
    )

DIAS_SEMANA = (
        ('SEG','Segunda'),
        ('TER','Terça'),
        ('QUA','Quarta'),
        ('QUI','Quinta'),
        ('SEX','Sexta'),
        ('SAB','Sábado'),
        ('DOM','Domingo')
    )

ESTADOS_VOO = (
     ('AGD','Agendado'),
     ('PRG','Programado'),
     ('EMB','Embarcando'),
     ('TAX','Taxiando'),
     ('PRT','Pronto'),
     ('AUT','Autorizado'),
     ('EMV','Em voo'),
     ('ATE','Aterrisado'),
     ('CAN','Cancelado'),
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
    
    @property
    def horario_chegada_base(self):
        time_delta_temp = datetime.timedelta(hours=self.duracao_base.hour, minutes=self.duracao_base.minute)
        horario_partida_base_temp = self.horario_partida_base
        
        #Workaround to add date and time
        start = datetime.datetime(
            2000, 1, 1,
            hour=horario_partida_base_temp.hour, 
            minute=horario_partida_base_temp.minute, 
            second=horario_partida_base_temp.second)
        end = start + time_delta_temp
        ####
        return end.time()

    class Meta:
        db_table = 'voo_base'

class VooReal(models.Model):    
    voo_base = models.ForeignKey(VooBase, on_delete=models.CASCADE, blank=True ,null=True)
    data_voo = models.DateField()
    estado_voo = models.CharField(max_length = 3, choices = ESTADOS_VOO, null=True, blank=True)
    horario_real_chegada = models.TimeField(auto_now=False, auto_now_add=False, null=True,blank=True)
    horario_real_partida = models.TimeField(auto_now=False, auto_now_add=False, null=True,blank=True)
    
    def clean(self):
        if self.horario_real_chegada and self.horario_real_partida :
            if self.horario_real_chegada < self.horario_real_partida: 
                raise ValidationError({
                                    'horario_real_chegada': ValidationError(('Horário de chegada não pode ser antes do horário de partida'), code='Invalid value'),
                                    'horario_real_partida': ValidationError(('Horário de chegada não pode ser antes do horário de partida'), code='invalid value'),
                })

    class Meta:
        db_table = 'voo_real'