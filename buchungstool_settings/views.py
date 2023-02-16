from django.shortcuts import render, redirect
from .forms import SettingForm, InfoFrontpageForm, Setting
import os
from mysite.settings import MEDIA_ROOT


def settings(request):
    obj, created = Setting.objects.get_or_create(name='settings')
    # If created True -> First start -> show settings
    if obj.logo:
        filepath = str(obj.logo.file)
    else:
        filepath = None
    if request.method == 'GET':
        f = SettingForm(instance=obj)
        return render(request, 'buchungstool_settings.html', {'form': f})

    if request.method == 'POST':
        f = SettingForm(request.POST, request.FILES, instance=obj)
        if f.is_valid():
            if request.FILES.get('logo') and filepath is not None:
                try:
                    os.remove(filepath)
                except FileNotFoundError:
                    print("No file to delete.")
            f.save()

        return redirect('settings')


def settings_frontpage_alert(request):
    obj, created = Setting.objects.get_or_create(name='settings_frontpage_alert')
    # If created True -> First start -> show settings
    if request.method == 'GET':
        f = InfoFrontpageForm(instance=obj)
        return render(request, 'buchungstool_settings_frontpage_alert.html', {'form': f})

    if request.method == 'POST':
        f = InfoFrontpageForm(request.POST, instance=obj)
        if f.is_valid():
            f.save()
        return redirect('settings_frontpage_alert')
