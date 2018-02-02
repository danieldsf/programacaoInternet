from django.db import models

# Create your models here.

class Perfil(models.Model):
    
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null= False)
    email = models.CharField(max_length=255, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    
    contatos = models.ManyToManyField("Perfil")

    def convidar(self, perfil_convidado):
        convite = Convite(solicitante=self,convidado = perfil_convidado)
        convite.save()

class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):
        self.convidado.contatos.add(self.solicitante)
        self.solicitante.contatos.add(self.convidado)
        self.delete()