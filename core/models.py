from django.db import models

from django.contrib.auth.models import User

class AlunoCollege(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_ativo = models.BooleanField(default=False)
    id_assinatura = models.CharField(max_length=255, blank=True, null=True, help_text="ID do assinante no Mercado Pago")

    def __str__(self):
        return f"{self.user.username} - Ativo: {self.is_ativo}"

class Aula(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    url_video = models.URLField(help_text="URL do vídeo (ex: YouTube ou Vimeo)")
    data_publicacao = models.DateTimeField(auto_now_add=True)
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição da aula")

    class Meta:
        ordering = ['ordem', 'data_publicacao']

    def __str__(self):
        return self.titulo
