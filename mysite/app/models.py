import datetime
from django.db import models

class VooBase(models.Model):
    codigo_voo = models.CharField(max_length=200, null=False)
    compania_aerea = models.CharField(max_length=200, null=False)
    dia_da_semana = models.CharField(max_length=200, null=False)
    horario_partida_base = models.CharField(max_length=200, null=False)
    duracao_base = models.CharField(max_length=200, null=False)
    origem = models.CharField(max_length=200, null=False)
    destino = models.CharField(max_length=200, null=False)

    class Meta:
        db_table = 'voo_base'

class VooReal(models.Model):
    ESTADOS_VOO = (
     ('EMB','Embarcando'),
     ('CAN','Cancelado'),
     ('PRG','Programado'),
     ('TAX','Taxiando'),
     ('PRT','Pronto'),
     ('AUT','Autorizado'),
     ('EMV','Em voo'),
     ('ATE','Aterrisado'),
    )
    
    voo_base = models.ForeignKey(VooBase, on_delete=models.CASCADE)
    data_voo = models.DateField()
    estado_voo = models.CharField(max_length = 1, choices = ESTADOS_VOO)
    horario_real_chegada = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    horario_real_partida = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    
    class Meta:
        db_table = 'voo_real'