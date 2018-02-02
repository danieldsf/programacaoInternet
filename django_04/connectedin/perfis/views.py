from django.shortcuts import render
from perfis.models import *
from django.shortcuts import redirect
# Create your views here.

perfil_id = 1

def index(request):
	return render(request, 'index.html', 
		{'perfis' :Perfil.objects.all(),
		'perfil_logado' : get_perfil_logado(request)})

def exibir(request, perfil_id):
	perfil = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	ja_eh_contato = perfil in perfil_logado.contatos.all()

	ja_foi_convidado = Convite.objects.filter(solicitante=perfil_logado, convidado=perfil)

	return render(request, 'perfil.html',
		          {'perfil' : perfil,
		          'perfil_logado' : perfil_logado,
		          'ja_eh_contato' : ja_eh_contato,
		          'ja_foi_convidado': ja_foi_convidado})

def convidar(request, perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_logado.convidar(perfil_id)

	return  redirect('index')

def desfazer(request, perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_logado.desfazer(perfil_id)

	return  redirect('index')

def get_perfil_logado(request):
	return Perfil.objects.get(id=perfil_id)

def aceitar(request, convite_id):
	convite = Convite.objects.get(id=convite_id)
	convite.aceitar()

	return redirect('index')

def recusar(request, convite_id):
	convite = Convite.objects.get(id=convite_id)
	convite.recusar()

	return  redirect('index')

def logout(request):
	global perfil_id
	if(perfil_id == 3):
		perfil_id = 1
	else:
		perfil_id += 1

	return redirect('index')