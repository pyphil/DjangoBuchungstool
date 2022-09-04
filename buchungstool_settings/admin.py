from django.contrib import admin
from .models import Config


class ConfigCustomAdmin(admin.ModelAdmin):
    list_display = ('name', 'setting')


admin.site.register(Config, ConfigCustomAdmin)
