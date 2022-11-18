from dataclasses import fields
from django import forms
from app.models import DIAS_SEMANA, VooBase, VooReal

class VooBaseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo_voo'].widget.attrs.update({'placeholder':'CEE3100'})
        self.fields['horario_partida_base'].widget.attrs.update({'placeholder':'HH:MM'})
        self.fields['duracao_base'].widget.attrs.update({'placeholder':'HH:MM'})

        self.fields['horario_partida_base'].widget.attrs.update({'placeholder':'HH:MM'})
            
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

class VooRealForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_voo'].widget.attrs.update({'placeholder':'DD-MM-AAAA'})
        self.fields['data_voo'].input_formats = [ '%d-%m-%Y' ]

        self.fields['horario_real_chegada'].widget.attrs.update({'placeholder':'HH:MM'})
        self.fields['horario_real_partida'].widget.attrs.update({'placeholder':'HH:MM'})
    
    class Meta:
        model = VooReal
        fields = (
            'data_voo',
            'estado_voo',
            'horario_real_chegada',
            'horario_real_partida')
        labels = {
            'data_voo':'Data de partida',
            'estado_voo':'Estado do voo',
            'horario_real_chegada':'Horario de chegada',
            'horario_real_partida':'Horario de partida',
        }