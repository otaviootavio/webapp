from dataclasses import fields
from django import forms
from app.models import DIAS_SEMANA, VooBase

class VooBaseForm(forms.ModelForm):
    
    class Meta:
        model = VooBase
        fields = ('codigo_voo',
                  'companhia_aerea',
                  'dia_da_semana',
                  'horario_partida_base',
                  'duracao_base',
                  'origem',
                  'destino')
        labels = {
            'codigo_voo':'Código Voo',
            'companhia_aerea':'Companhia Aerea',
            'dia_da_semana':'Dia da semana',
            'horario_partida_base':'Horario de partida',
            'duracao_base':'Duração',
            'origem':'Origem',
            'destino':'Destino'
        }
        