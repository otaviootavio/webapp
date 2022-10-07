import datetime
from app.models import VooBase, VooReal
from django.test import TestCase
# Create your tests here.

class VooBaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        VooBase.objects.create(
                        codigo_voo = "1234",
                        compania_aerea = "1234",
                        dia_da_semana = 'SEG',
                        horario_partida_base = datetime.time(5,0,0),
                        duracao_base = datetime.time(1,1,1),
                        origem = "Brasilia",
                        destino = "Guarulhos")
        VooBase.objects.create()
    
    def test_criacao_voo_base(self):
        voo_1 = VooBase.objects.get(codigo_voo="1234")
        self.assertEqual(voo_1.codigo_voo, "1234")