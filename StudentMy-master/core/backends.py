from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db import transaction
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth, messages
from .models  import *
from .decorators  import *
from .forms   import *

def get_current_user(request):
    current_id = request.session.get('user')['id']
    user = User.objects.filter(pk=current_id).first()

    if(user.who_is == 'ST'):
        return Student.objects.filter(pk=current_id).first()
    else:
        return Teacher.objects.filter(pk=current_id).first()


#I love you Daniel S2:
@class_view_decorator(login_required)
class GenericFormView(View):
    form = ''
    model = ''
    name = ''
    caption = ''
    redirect_url_form = ''

    def get_target_url(self, id):
        if id is not None:
            return '/%s/%s/%d' % (self.name, 'edit', id)
        return '/%s/%s' % (self.name, 'add')
    
    def get_caption(self, id):
        if id is not None:
            return 'Editar %s' % (self.caption)
        return 'Adicionar %s' % (self.caption)    

    def get(self, request, id = None):
        if(id is None):
            return render(request, 'generics/form.html', {'form': self.form(), 'caption': self.get_caption(id), 'target_url': self.get_target_url(id)})
        else:
            entity = get_object_or_404(self.model, pk=id)
            form = self.form(None, instance=entity)
            return render(request, 'generics/form.html', {'form': form, 'caption': self.get_caption(id), 'target_url': self.get_target_url(id)})

    def post(self, request, id = None):
        if(id is None):
            form = self.form(request.POST, request.FILES)
            if form.is_valid():
                feedback = form.save()
                
                if(feedback):
                    messages.success(request, 'Registro cadastrado com sucesso')
                    return redirect(self.redirect_url_form)
                else:
                    messages.warning(request, 'Erro no cadastro')

            else:
                messages.warning(request, 'Erro no cadastro do registro!')
                return render(request, 'generics/form.html', {'form': form, 'caption': self.get_caption(id), 'target_url': self.get_target_url(id)})
        else:
            entity = get_object_or_404(self.model, pk=id)
            form = self.form(request.POST, request.FILES or None, instance=entity)
            if form.is_valid():
                feedback = form.save()

                if(feedback):
                    messages.success(request, 'Registro cadastrado com sucesso')
                    return redirect(self.redirect_url_form)
                else:
                    messages.warning(request, 'Erro no cadastro')
                
                #messages.success(request, 'Registro editado com sucesso')
                return redirect(self.redirect_url_form)
            else:
                messages.warning(request, 'Erro na edicao do registro')
                return render(request, 'generics/form.html', {'form': form, 'caption': self.get_caption(id), 'target_url': self.get_target_url(id)})

# Daniel, you are so nice :) :
@login_required
def generic_delete(request, id, entity, redirect_url_delete):
    object_data = entity.objects.filter(pk=id).first()

    if(object_data is not None):
        if(object_data.delete()):
            messages.success(request, 'Registro deletado com sucesso')
        else:
            messages.warning(request, 'Erro na delecao')
    else:
        messages.warning(request, 'Registro inexistente')

    return redirect(redirect_url_delete)

# Create your views here.
class LoginView(View):
    form = LoginForm
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = {'id': user.id, 'name': user.first_name, 'who_is': user.who_is}
                return redirect('/dashboard')
            else:
                messages.warning(request, 'Conta desabilitada!')
                return redirect('/login')
        else:
            messages.warning(request, 'E-mail ou senha errados, tente novamente!')
            return redirect('/login')

class RegistrarUsuarioView(View):
    form = RegistrarUsuarioForm
    template_name = 'users/sign-up.html'

    def get(self,request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self,request):
        form = self.form(request.POST)

        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = form.save(commit=False)
            usuario.is_staff = True
            usuario.is_superuser = True
            usuario.username = usuario.email
            usuario.save()
            
            instancia = None
            
            if(dados_form['who_is'] == 'ST'):
                instancia = Student(user=usuario, name=dados_form['first_name'])
            else:
                instancia = Teacher(user=usuario, name=dados_form['first_name'])
            
            instancia.save()

            return redirect('index')

        return render(request, self.template_name, {'form': form})

@class_view_decorator((login_required, teacher_required))
class CourseFormView(GenericFormView):
    form = CourseForm
    template_name = 'courses/add.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        
        if form.is_valid():
            dados_form = form.cleaned_data
            curso = form.save(commit=False)
            curso.teacher = get_current_user(request)
            curso.save()
            return redirect('/dashboard')

        return render(request, self.template_name, {'form': form})            


@class_view_decorator((login_required, teacher_required))
class LectureFormView(GenericFormView):
    form = LectureForm
    template_name = 'lectures/add.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        
        if form.is_valid():
            dados_form = form.cleaned_data
            curso = form.save(commit=False)
            curso.save()
            return redirect('/dashboard')

        return render(request, self.template_name, {'form': form})


@class_view_decorator((login_required, teacher_required))
class DiscountFormView(GenericFormView):
    form = DiscountForm
    template_name = 'discount/add.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        
        if form.is_valid():
            dados_form = form.cleaned_data
            curso = form.save(commit=False)
            curso.save()
            return redirect('/dashboard')

        return render(request, self.template_name, {'form': form})    