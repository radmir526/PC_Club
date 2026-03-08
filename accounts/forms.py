from django import forms
from .models import CustomUser

# Используем ModelForm, она автоматически сохраняет данные в базу, через метод save()
class RegisterForm(forms.ModelForm):
    # Эти два поля мы создаем вручную, потому что их нет в модели
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    # Класс мета использует модель CustomUser
    class Meta:
        model = CustomUser
        fields = ['phone', 'first_name', 'password'] # пользователю будут показаны эти поля

    # Метод clean автоматом выполняет проверки, сначала базовые Django условно на пустоту поля
    def clean(self):
        cleaned_data = super().clean()
        
        # Берем значение по ключу, если его нет, то вернется None
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # А потом наша проверка на совпадение паролей
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        
        return cleaned_data
    
# форма для входа в профиль, просто находятся такие поля в базе данных
class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    
    