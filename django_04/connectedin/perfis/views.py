from django.shortcuts import render
from perfis.models import Perfil
from django.shortcuts import redirect
# Create your views here.

def index(request):
	return render(request, 'index.html', 
		{'perfis' :Perfil.objects.all(),
		'perfil_logado' : get_perfil_logado(request)})

def exibir(request, perfil_id):
	perfil = Perfil.objects.get(id=perfil_id)

	return render(request, 'perfil.html',
		          {'perfil' : perfil,
		          'perfil_logado' : get_perfil_logado(request)})


def get(perfil_id):
	if (perfil_id == 1):
		return Perfil('Ely', 'ely@ifpi.edu.br',
						'99999-9999', 'ifpi')				
	if (perfil_id == 2):
		return Perfil('Pedro', 'pedro@gmail.com',
						'99999-8888', 'Google')				
	if (perfil_id == 3):
		return Perfil('Maria', 'maria@hotmail.com',
						'88888-7777', 'MS')	

def convidar(request,perfil_id):

	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	perfil_logado.convidar(perfil_a_convidar)

	return  redirect('index')

def get_perfil_logado(request):
	return Perfil.objects.get(id=1)

def aceitar(request, convite_id):
	convite = Convite.objects.get(id=convite_id)
	convite.aceitar()
	return redirect('index')