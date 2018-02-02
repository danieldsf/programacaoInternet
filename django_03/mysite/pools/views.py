from django.shortcuts import render
from .models import *
# INDEX
def index(request):
	return render(request, 'index.html', {'title': 'Index'})

# Question INDEX
def question(request):
	return render(request, 'question.html', {'data': Question.objects.all()})	

# Question INDEX
def question_detail(request, id):
	return render(request, 'question_detail.html', {'data': Question.objects.get(pk=id)})	