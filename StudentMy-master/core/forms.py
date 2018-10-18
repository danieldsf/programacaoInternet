from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from core.models import *

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'validate','placeholder': 'Email : aluno@gmail.com'}),label="", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Senha'}), label="", max_length=100)

class CaseInsensitiveUserCreationForm(UserCreationForm):
    def clean(self):
        cleaned_data = super(CaseInsensitiveUserCreationForm, self).clean()
        username = cleaned_data.get('username')

        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        
        return cleaned_data

class RegistrarUsuarioForm(CaseInsensitiveUserCreationForm):
    username = forms.CharField(widget = forms.HiddenInput(), required = False)
    # código omitido
    def is_valid(self):
        valid = True

        if not super(RegistrarUsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados informados')
            valid = False

        user_exists = User.objects.filter(email=self.cleaned_data['email']).exists()
        
        if user_exists:
            self.adiciona_erro('Usuário já existente.')
            valid = False

        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)
    
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email', 'who_is', 'password1', 'password2')   

class RecoverPasswordForm(forms.Form):
    email = forms.CharField(required=True)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('thumb', 'name', 'price', 'contents')

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('thumb', 'name', 'course', 'url')

class DiscountForm(forms.ModelForm):
    class Meta:
        model = DiscountCoupon
        fields = ('discount_type', 'value', 'expiration_date', 'course')

    