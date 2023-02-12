from django.shortcuts import render, redirect
from .forms import SettingForm, Setting


def settings(request):
    obj, created = Setting.objects.get_or_create(name='settings')
    # If created True -> First start -> show settings
    if request.method == 'GET':
        f = SettingForm(instance=obj)
        return render(request, 'buchungstool_settings.html', {'form': f})

    if request.method == 'POST':
        f = SettingForm(request.POST, instance=obj)
        if f.is_valid():
            f.save()
        return redirect('settings')
