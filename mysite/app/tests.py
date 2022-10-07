from app.models import Livro, Usuario, Emprestimo
from django.test import TestCase
# Create your tests here.

class LivroModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Livro.objects.create(titulo='Os Irmãos Karamazov',isbn='000000')
    def test_criacao_id(self):
        livro_1 = Livro.objects.get(titulo='Os Irmãos Karamazov')
        self.assertEqual(livro_1.id, 1)