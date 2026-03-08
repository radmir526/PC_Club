from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'first_name', 'is_staff', 'is_active',
                    'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['phone', 'first_name']


