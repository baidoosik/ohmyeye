from django.contrib import admin
from .models import EyeInfomation
# Register your models here.


@admin.register(EyeInfomation)
class EyeInfomationModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile']
    list_display_links = ['id', 'profile']

