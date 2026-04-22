from django.db import models
from django.utils import timezone


class Incidente(models.Model):

    SISTEMA_CHOICES = [
        ('Portal do Aluno', 'Portal do Aluno'),
        ('Lyceum', 'Lyceum'),
        ('Chamada', 'Chamada'),
    ]

    STATUS_CHOICES = [
        ('Funcionando', 'Funcionando'),
        ('Instável', 'Instável'),
        ('Fora do Ar', 'Fora do Ar'),
    ]

    PRIORIDADE_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Média'),
        ('baixa', 'Baixa'),
    ]

    sistema = models.CharField(max_length=50, choices=SISTEMA_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Funcionando')
    descricao = models.TextField()
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    data_criacao = models.DateTimeField(default=timezone.now)
    resolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sistema} - {self.status}"