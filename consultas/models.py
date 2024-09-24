from django.db import models


class TipoConsulta(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=False, blank=False)
    preco = models.FloatField()

    def __str__(self) -> str:
        return self.nome


class Consulta(models.Model):
    nome_paciente = models.CharField(max_length=100)
    idade = models.IntegerField()
    data_consulta = models.DateTimeField()
    tipo = models.ForeignKey(TipoConsulta, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.nome_paciente} | {self.tipo} | {self.data_consulta}"
