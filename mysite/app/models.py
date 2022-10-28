from django.db import models

class VooBase(models.Model):
    DIAS_SEMANA = (
        ('SEG','Segunda'),
        ('TER','Terca'),
        ('QUA','Quarta'),
        ('QUI','Quinta'),
        ('SEX','Sexta'),
        ('SAB','Sabado'),
        ('DOM','Domingo')
    )
    codigo_voo = models.CharField(max_length=200, null=False)
    companhia_aerea = models.CharField(max_length=200, null=False)
    dia_da_semana = models.CharField(max_length = 3, choices = DIAS_SEMANA)
    horario_partida_base = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    duracao_base = models.IntegerField(null=False)
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
    estado_voo = models.CharField(max_length = 3, choices = ESTADOS_VOO)
    horario_real_chegada = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    horario_real_partida = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    
    class Meta:
        db_table = 'voo_real'