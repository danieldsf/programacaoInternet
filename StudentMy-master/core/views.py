from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .backends import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core import mail

def index(request):
    if(request.session.get('user')):
        return redirect('/dashboard')
    return render(request, 'main.html')

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


def logout_view(request):
    messages.success(request, 'Logout realizado com sucesso!')
    logout(request)
    return HttpResponseRedirect('/login')

def handler404(request, exception, template_name='generics/error.html'):
    context = {'message': 'Not found'}
    return render(request, template_name, context, status=404)
    
def handler500(request, template_name='generics/error.html'):
    context = {'message': 'Server Error'}
    return render(request, template_name, context, status=500)

def course_list(request):
    context = {
        'courses': Course.objects.all(),
    }

    return render(request, 'course/list-aluno.html', context)

@student_required
def favorites_list(request):
    context = {
        'courses': get_current_user(request).subscriptions.filter(is_favorite=True),
    }

    return render(request, 'course/list-course-favorite.html', context)

@teacher_required
def subscriptions_list(request):
    teacher = get_current_user(request)

    context = {
        'subscriptions': Subscription.objects.filter(course__teacher=teacher)
    }

    return render(request, 'course/list-subscriptions.html', context)

def course_list_teacher(request):
    context = {
        'courses': Course.objects.all(),
    }
    return render(request, 'course/list-professor.html',context)

@student_required
def course_details(request, id):
    context = {
        'course': Course.objects.filter(pk=id).first(),
    }
    return render(request, 'course/detail_course.html', context)

@student_required
def view_lectures(request, id):
    curso = Course.objects.filter(pk=id).first()
    context = {
        'name': curso.name,
        'thumb': curso.thumb,
        'lectures': curso.lectures.all(),
    }

    return render(request, 'course/list-lectures.html', context)

def buy_course(request, id):
    student = get_current_user(request)
    feedback = student.buy_course(id)

    if feedback:
        messages.success(request, 'Course pending for aproval!')
    else:
        messages.error(request, 'Course already bought!')

    return redirect('/dashboard')

def aprove_subscription(request, id):
    teacher = get_current_user(request)
    feedback = teacher.set_course_payment(id)

    if feedback:
        messages.success(request, 'Subscription aproved for aproval!')
    else:
        messages.error(request, 'Not possible to change subscription status!')

    return redirect('/dashboard')    

def buy_course_confirmation(request,id):
    context = {
        'course': Course.objects.filter(pk=id).first(),
    }
    return render(request, 'course/buy-course.html',context)

def favorite_course(request, id):
    student = get_current_user(request)
    student.favorite_course(id)
    messages.success(request, 'Course set as favorite!')
    return redirect('/dashboard')

def rate_course(request, id):
    student = get_current_user(request)
    student.rate_course(id)
    return redirect('/dashboard')

#pass