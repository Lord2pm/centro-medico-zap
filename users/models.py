from django.db import models


class User(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=30, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nome
