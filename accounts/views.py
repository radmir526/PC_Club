from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from .models import CustomUser
from .forms import RegisterForm, LoginForm


class RegisterView(View):
    # Get запрос показываем пустую форму
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
    
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'accounts/partials/register.html', {'form': form})
        return TemplateResponse(request, 'accounts/register.html', {'form': form})
    
    # POST Запос, пользователь отправил форму
    def post(self, request):
        form = RegisterForm(request.POST)
        
        # Если форма валидна, то мы
        if form.is_valid():
            user = form.save(commit=False) # Создаем пользователя, но пока не сохраняем
            user.set_password(form.cleaned_data['password']) # Хешируем пароль
            user.save()
            login(request, user) # Сразу заходим в профиль
            if request.headers.get('HX-Request'):
                return TemplateResponse(request, 'accounts/partials/profile.html', {'user':request.user})  # Возвращаем страницу профиля
            return TemplateResponse(request, 'accounts/profile.html', {'user': request.user})
        # Если форма не правильная, то возвращаем ее снова, но с ошибками
        return TemplateResponse(request, 'accounts/register.html', {'form': form})
    
    
# Класс для входа в профиль
class LoginView(View):
    # Так же выдаем пустую форму для заполнения
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'accounts/partials/login.html', {'form': form})
        return TemplateResponse(request, 'accounts/login.html', {'form': form})

    # Пользователь отправляет форму    
    def post(self, request):
        form = LoginForm(request.POST)
        
        # Если форма валидна
        if form.is_valid():
            # Достаем с базы данные
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            # Сравниваем их с введенными пользователем
            user = authenticate(request, username=phone, password=password)

            # Если пользователь найден, то автоматический вход в акк
            if user is not None:
                login(request, user)
                if request.headers.get('HX-Request'):
                    return TemplateResponse(request, 'accounts/partials/profile.html', {'user': user})
                return TemplateResponse(request, 'accounts/profile.html', {'user': request.user})
            else: # Если нет, то выдаем ошибку
                form.add_error(None, 'Неверный пароль или номер')
        # Если форма не валидна, то выводим ошибку и еще раз страницу заполнения
        return TemplateResponse(request, 'accounts/login.html', {'form': form})
    

# Класс для выхода из профиля
class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('club:index')
    

# Если юзер не залогинен, то LoginRequiredMixin его автоматически перенаправит
# На страницу входа
class ProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    # Если залогинен, то открывается страница пользователя
    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'accounts/partials/profile.html', {'user': request.user})
        return TemplateResponse(request, 'accounts/profile.html', {'user': request.user})