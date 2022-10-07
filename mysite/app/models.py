import datetime
from django.db import models

class Livro(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200, null=False)
    isbn = models.CharField(max_length=20, null=False, unique=True)

    class Meta:
        db_table = 'livros'

class Usuario(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200, null=False)
    
    class Meta:
        db_table = 'usuarios'

class Emprestimo(models.Model):
    id = models.IntegerField(primary_key=True)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now=True)
    prazo = models.DurationField(default=datetime.timedelta(days=7))
    data_devolucao = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'emprestimos'