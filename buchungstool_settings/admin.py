from django.contrib import admin
from .models import Config, Setting


class ConfigCustomAdmin(admin.ModelAdmin):
    list_display = ('name', 'setting')


admin.site.register(Config, ConfigCustomAdmin)
admin.site.register(Setting)
