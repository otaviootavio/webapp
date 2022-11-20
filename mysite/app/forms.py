from dataclasses import fields
from django import forms
from app.models import VooBase, VooReal, ESTADOS_VOO

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
        self.fields['horario_real_partida'].widget.attrs.update({'placeholder':'HH:MM'})
        self.fields['horario_real_chegada'].widget.attrs.update({'placeholder':'HH:MM'})
    
    def clean(self):
        cleaned_data = super().clean()
        estado_antigo = VooReal.objects.get(voo_base = self.data['voo_base'] ).estado_voo
        num_estado_antigo = int(list(map(lambda x: x[0],list(ESTADOS_VOO))).index(estado_antigo))
        estado_novo = cleaned_data.get("estado_voo")
        num_estado_novo = int(list(map(lambda x: x[0],list(ESTADOS_VOO))).index(estado_novo))
        
        if(num_estado_novo != num_estado_antigo + 1 and num_estado_novo != len(ESTADOS_VOO) - 1):
            self.add_error('estado_voo', "Estado invalido, siga a ordem correta")
        
        if(estado_novo == "EMV" and cleaned_data.get("horario_real_partida") is None):
            self.add_error('horario_real_partida', "O horário é obrigatório")
            if(cleaned_data.get("horario_real_chegada") is not None):
                self.add_error('horario_real_partida', "Preencha apenas na aterrissagem")
            
        if(estado_novo == "ATE" and cleaned_data.get("horario_real_chegada") is None):
            self.add_error('horario_real_chegada', "O horário é obrigatório")
            
    class Meta:
        model = VooReal
        fields = (
            'voo_base',
            'data_voo',
            'estado_voo',
            'horario_real_partida',
            'horario_real_chegada')
        labels = {
            'data_voo':'Data de partida',
            'estado_voo':'Estado do voo',
            'horario_real_partida':'Horario de partida',
            'horario_real_chegada':'Horario de chegada',
        }
        widgets = {
            'voo_base': forms.HiddenInput(),
        }