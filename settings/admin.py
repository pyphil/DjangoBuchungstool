import imp
from django.contrib import admin
from .models import Setting


class SettingCustomAdmin(admin.ModelAdmin):
    list_display = ('name', 'setting')


admin.site.register(Setting, SettingCustomAdmin)
