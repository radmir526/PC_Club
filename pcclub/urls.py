from django.contrib import admin  # Импортируем админку Django, чтобы можно было использовать встроенный интерфейс администратора
from django.urls import path, include  # Импортируем функции для маршрутизации: path — для конкретных URL, include — для подключения других URL-конфигов
from django.conf import settings  # Импортируем настройки проекта, чтобы проверять DEBUG и другие параметры
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('club.urls', namespace='club')),
    path('accounts/', include('accounts.urls', namespace='accounts'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
