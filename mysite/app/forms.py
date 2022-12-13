from dataclasses import fields
from django import forms
from app.models import VooBase, VooReal, ESTADOS_VOO

class VooBaseForm(forms.ModelForm):
    data_voo = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'),input_formats=['%d-%m-%Y'])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_voo'].widget.attrs.update({'placeholder':'DD-MM-AAAA'})
        self.fields['data_voo'].input_formats = [ '%d-%m-%Y' ]
        self.fields['codigo_voo'].widget.attrs.update({'placeholder':'CEE3100'})
        self.fields['horario_partida_base'].widget.attrs.update({'placeholder':'HH:MM'})
        self.fields['duracao_base'].widget.attrs.update({'placeholder':'HH:MM'})

        self.fields['horario_partida_base'].widget.attrs.update({'placeholder':'HH:MM'})
    
    def clean(self):
        cleaned_data = super().clean()
        cidade_origem = cleaned_data.get("origem")
        cidade_destino = cleaned_data.get("destino")
        
        
        if(cidade_origem != 'SP' and cidade_destino != 'SP'):
            self.add_error('origem', "O voo deve conter SP em sua trajetoria")
            self.add_error('destino', "O voo deve conter SP em sua trajetoria")                
            
    class Meta:
        model = VooBase
        fields = ('codigo_voo',
                  'companhia_aerea',
                  'horario_partida_base',
                  'duracao_base',
                  'data_voo',
                  'origem',
                  'destino')
        labels = {
            'codigo_voo':'Código Voo',
            'companhia_aerea':'Companhia Aerea',
            'data_voo':'Data do voo',
            'horario_partida_base':'Horario de partida',
            'duracao_base':'Duração',
            'origem':'Origem',
            'destino':'Destino'
        }

class VooRealForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario_real_partida'].widget.attrs.update({'placeholder':'HH:MM'})
        self.fields['horario_real_chegada'].widget.attrs.update({'placeholder':'HH:MM'})
    
    def clean(self):
        cleaned_data = super().clean()
        estado_novo = cleaned_data.get("estado_voo")
        num_estado_novo = int(list(map(lambda x: x[0],list(ESTADOS_VOO))).index(estado_novo))
            
        if(self.instance.id and VooReal.objects.get(id = self.instance.id ).estado_voo != None):
            estado_antigo = VooReal.objects.get(id = self.instance.id ).estado_voo
            num_estado_antigo = int(list(map(lambda x: x[0],list(ESTADOS_VOO))).index(estado_antigo))
            if(estado_novo != "CAN" and num_estado_novo != num_estado_antigo + 1):
                self.add_error('estado_voo', "Estado invalido, siga a ordem correta")
        
        origem = cleaned_data.get("voo_base").origem
        destino = cleaned_data.get("voo_base").destino
        
    
        if not (VooReal.objects.get(id = self.instance.id ).estado_voo):
            if(origem == 'SP' and estado_novo != 'Embarcando'):
                self.add_error('estado_voo', "Todos os voos de partida devem começar em embarcando")
            
            if(destino == 'SP'and estado_novo != 'Em voo'):
                self.add_error('estado_voo', "Todos os voos de chegada devem começar em voo")
        
        if(estado_novo != "Cancelado" ):
            if(estado_novo == "Em voo" and cleaned_data.get("horario_real_partida") is None):
                self.add_error('horario_real_partida', "O horário é obrigatório")
            
            if(estado_novo != "Em voo" and estado_novo != "Aterrisado" and cleaned_data.get("horario_real_partida") is not None):
                self.add_error('horario_real_partida', "O horário ainda não deve ser inserido")
            
            if(estado_novo != "Aterrisado" and cleaned_data.get("horario_real_chegada") is not None):
                self.add_error('horario_real_chegada', "O horário ainda não deve ser inserido")
            
            if(estado_novo == "Aterrisado" and cleaned_data.get("horario_real_chegada") is None):
                self.add_error('horario_real_chegada', "O horário é obrigatório")
            
    class Meta:
        model = VooReal
        fields = (
            'voo_base',
            'estado_voo',
            'horario_real_partida',
            'horario_real_chegada')
        labels = {
            'estado_voo':'Estado do voo',
            'horario_real_partida':'Horario de partida',
            'horario_real_chegada':'Horario de chegada',
        }
        widgets = {
            'voo_base': forms.HiddenInput(),
        }