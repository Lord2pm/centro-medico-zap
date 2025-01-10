from django.db import models

from users.models import User


class TipoConsulta(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=False, blank=False)
    preco = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nome


class Consulta(models.Model):
    nome_paciente = models.CharField(max_length=100)
    idade = models.IntegerField()
    data_consulta = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoConsulta, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.nome_paciente} | {self.tipo} | {self.data_consulta} | Usuário: {self.usuario.nome}"
