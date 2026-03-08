from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator


# Тут мы расширенного юзера и делаем проверки на данные
class CustomUserManager(BaseUserManager):
    # метод создания user
    def create_user(self, phone, first_name, password=None, **extra_fields):
        if not phone:
            raise ValueError('Телефон обязателен')

        if not first_name:
            raise ValueError('Имя обязательно')
        
        if not password:
            raise ValueError('Пароль обязателен')
        
        user = self.model(phone=phone, first_name=first_name, **extra_fields)

        user.set_password(password)

        user.full_clean() # Проверяем данные на валидность, логику и сразу запускаемя 
        user.save(using=self._db)

        return user
    

    def create_superuser(self, phone, first_name, password=None, **extra_fields):
        # Прописываем значение параметров по дефолту
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Проверка параметров
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(phone, first_name, password, **extra_fields)



# Класс, в котором мы создаем нашего юзера
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Тут мы прописываем валидатор для номера
    phone_validator = RegexValidator(
        regex=r'^\+?\d{9,100}$',
        message='Введите корректный номер телефона!'
    )
    # Прописываем саму модель телефона с автоматической проверкой на валидность
    phone = models.CharField(unique=True, max_length=100, validators=[phone_validator])
    first_name = models.CharField(max_length=100)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone' # Теперь вместо username будут вводить номер
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return f"{self.phone} - ({self.first_name})"