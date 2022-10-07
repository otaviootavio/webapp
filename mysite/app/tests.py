import datetime
from app.models import VooBase, VooReal
from django.test import TestCase
# Create your tests here.

class VooBaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        VooBase.objects.create(
                        codigo_voo = "1111",
                        compania_aerea = "Latam",
                        dia_da_semana = 'SEG',
                        horario_partida_base = datetime.time(5,0,0),
                        duracao_base = datetime.time(5,1,1),
                        origem = "Brasilia",
                        destino = "Maceio")
        
        VooBase.objects.create(
                        codigo_voo = "2222",
                        compania_aerea = "Latam",
                        dia_da_semana = 'SEG',
                        horario_partida_base = datetime.time(5,0,0),
                        duracao_base = datetime.time(20,1,1),
                        origem = "Brasilia",
                        destino = "Guarulhos")
        
        VooBase.objects.create(
                        codigo_voo = "3333",
                        compania_aerea = "Latam",
                        dia_da_semana = 'TER',
                        horario_partida_base = datetime.time(5,0,0),
                        duracao_base = datetime.time(10,1,1),
                        origem = "Brasilia",
                        destino = "Recife")
        
        VooBase.objects.create(
                        codigo_voo = "1122",
                        compania_aerea = "GOL",
                        dia_da_semana = 'SEG',
                        horario_partida_base = datetime.time(10,0,0),
                        duracao_base = datetime.time(2,1,1),
                        origem = "Brasilia",
                        destino = "Manaus")
        
        VooBase.objects.create(
                        codigo_voo = "9999",
                        compania_aerea = "GOL",
                        dia_da_semana = 'TER',
                        horario_partida_base = datetime.time(7,0,0),
                        duracao_base = datetime.time(1,30,1),
                        origem = "Brasilia",
                        destino = "Congonhas")
        
        VooBase.objects.create(
                        codigo_voo = "2020",
                        compania_aerea = "Azul",
                        dia_da_semana = 'SEG',
                        horario_partida_base = datetime.time(6,0,0),
                        duracao_base = datetime.time(2,1,1),
                        origem = "Brasilia",
                        destino = "Viracopos")
        VooBase.objects.create()
    
    def test_criacao_voo_base(self):
        voo_1 = VooBase.objects.get(codigo_voo="1111")
        self.assertEqual(voo_1.codigo_voo, "1111")
    
    def test_atualizacao_voo_base(self):
        voo_1 = VooBase.objects.get(codigo_voo="2222")
        voo_1.codigo_voo = "4200"
        self.assertEqual(voo_1.codigo_voo, "4200")
