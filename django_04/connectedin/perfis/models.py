from django.db import models

# Create your models here.

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null= False)
    email = models.CharField(max_length=255, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField("Perfil")

    def desfazer(self, perfil_id):
        perfil_a_desfazer = Perfil.objects.get(id=perfil_id)
        self.contatos.remove(perfil_a_desfazer)
        self.save()

    def convidar(self, perfil_id):
        perfil_a_convidar = Perfil.objects.get(id=perfil_id)

        if(self != perfil_a_convidar):
            convite = Convite(solicitante=self, convidado=perfil_a_convidar)
            convite.save()

class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def __str__(self):
        return 'Solicitante: %s - Convidado: %s' % (self.solicitante, self.convidado)

    def aceitar(self):
        self.convidado.contatos.add(self.solicitante)
        self.solicitante.contatos.add(self.convidado)
        self.delete()

    def recusar(self):
        self.delete()