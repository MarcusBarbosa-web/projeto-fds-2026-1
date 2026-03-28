from django.db import models
from django.utils import timezone



class Sistema(models.Model):
    STATUS_CHOICES = [
        ("operacional", "Operacional"),
        ("investigando", "Investigando"),
        ("indisponível", "Indisponível"),
        # 'operacional' -> Banco de Dados | 'Operacional' -> HTML
    ]

    nome = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="operacional"
    )

    def __str__(self) -> str:
        return str(self.nome)


# `max_length(100)`: O Django exige que CharField tenha um limite de tamanho. Isso funciona como uma medida de segurança, para que o banco de dados não gaste memória infinita. Em outras palavras: Se vinher alguém querendo causar uma falha no site e mandar hipertextos de +2000 caracteres, isso serve para barrar isso.
# `choices=STATUS_CHOICES`: Faz com que a coluna *Sistema* aceite ESTRITAMENTE os textos que estão na lista STATUS_CHOICES.
# `default=operacional`: Se alguém quiser cadastrar algo novo como "uaifai-apolo" e esquecer de dizer o status, o Django automaticamente vai colocar como operacional. Isso é muito útil, porquê se a pessoa esquece o Django dá uma falha bizonha.
# -------------------------------------------------------------------------------


class Incidente(models.Model):
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE)

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField(auto_now_add=True)

    resolvido = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"[{self.sistema.nome}] {self.titulo}"


# `on_delete=models.CASCADE`: Serve para se apagarmos algum sistema exemplo: uaifai-apolo, ele apagará todo o histórico de incidentes dele junto para não deixar o banco de dados sujo.
# `models.TextField()` -> Para textos longos e sem limite.
# `models.DateTimeField(auto_now_add=True) -> Pra gente saber a data e hora exata em que algo caiu, quando registrarem um incidente o `auto_now_add` vai pegar a data do sistema sozinho e guardar.
# -------------------------------------------------------------------------------

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

    sistema = models.CharField(max_length=50, choices=SISTEMA_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.sistema} - {self.status}"