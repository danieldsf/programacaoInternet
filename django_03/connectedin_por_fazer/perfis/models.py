from django.db import models

# Create your models here.

class Perfil(models.Model):
	nome = models.CharField(max_length=255, null=False)
	email = models.CharField(max_length=255, null=False)
	telefone = models.CharField(max_length=255, null=False)
	nome_empresa = models.CharField(max_length=255, null=False)

	def convidar(self, perfil_convidado):
		convite = Convite(solicitante = self, convidado = perfil_convidado)
		convite.save()

class Convite(models.Model):
	solicitante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="convites_feitos")
	convidado = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="convites_recebidos")