from django.shortcuts import render
from .models import *
from django.http import HttpResponse
# Create your views here.
def check_method(callBack):
	try:
		return HttpResponse('Return: %' % (callBack()))
	except Exception as e:
		return HttpResponse('Error when performing method: %s' % e)

def add(request):
	return check_method(add_action)

def create(request):
	return check_method(create_action)

def clear(request):
	return check_method(clear_action)

def set(request):
	return check_method(set_action)

def remove(request):
	return check_method(remove_action)

'''HEHE'''
def warmup(request):
	for i in range(25):
		blog = Blog(name = 'Blog do Joao Bidu')
		blog.save()
		entry = Entry(body_text='Haha', headline='Hehe', blog=blog)
		entry.save()
		entry = Entry(body_text='Hihi', headline='Hoho', blog=blog)
		entry.save()

	return HttpResponse('Warmup done')


def create_action():
	blog = Blog(name = 'Blog do Joao Bidu')
	blog.save()

	entry = blog.entry_set.create(body_text='Haha', headline='HEHE')

	return len(blog.entry_set.all()) > 0

def add_action():
	blog = Blog.objects.all()[0]
	entry = Entry.objects.all()[0]

	last_value = len(blog.entry_set)
	
	blog.entry_set.add(entry)
	print(blog.entry_set)
	return last_value < len(blog.entry_set)

def clear_action():
	blog = Blog.objects.all()[0]
	blog.entry_set.clear()

	return len(blog.entry_set) == 0

def set_action():
	blog = Blog(name = 'Blog do Joao Bidu')

	entry1 = Entry.objects.all()[0]
	entry2 = Entry.objects.all()[1]

	entries = [entry1, entry2]

	blog.entry_set.set(entries)

	return len(blog.entry_set) == 0

def remove_action():
	blog = Blog.objects.all()[0]
	entry = Entry.objects.all()[0]

	blog.entry_set.remove(entry)

	return last_value > len(Blog.objects.all())