from django.shortcuts import render
from django.core import serializers
from .models import *

# Create your views here.
def index(request):
	return render(request, 'index.html', {'title': 'Index'});

#Utils:
def get_json(classname):
    return serializers.serialize('json', classname.objects.all())

class Printer(object):
    @staticmethod
    def users(request):
        return render(request, 'generic_list.html', {'title': 'Users', 'data': get_json(User)});

    @staticmethod
    def profiles(request):
        return render(request, 'generic_list.html', {'title': 'Profiles', 'data': get_json(Profile)});

    @staticmethod
    def postreactions(request):
        return render(request, 'generic_list.html', {'title': 'PostReactions', 'data': get_json(PostReaction)});

    @staticmethod
    def posts(request):
        return render(request, 'generic_list.html', {'title': 'Posts', 'data': get_json(Post)});

    @staticmethod
    def comments(request):
        return render(request, 'generic_list.html', {'title': 'Comments', 'data': get_json(Comment)});

    @staticmethod
    def reactions(request):
        return render(request, 'generic_list.html', {'title': 'Reactions', 'data': get_json(Reaction)});