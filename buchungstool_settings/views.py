from django.shortcuts import render, redirect
from .forms import SettingForm, InfoFrontpageForm, Setting, CategoryForm, RoomForm
from buchungstool.models import Category, Room
import os
from django.forms import modelformset_factory
from django import forms

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


def category_setup(request, new=0):
    obj = Category.objects.all()
    CategoryFormset = modelformset_factory(Category, form=CategoryForm, extra=new)

    if request.method == 'GET':
        formset = CategoryFormset(queryset=obj)
        return render(request, 'buchungstool_settings_category_setup.html', {'categories': obj, 'formset': formset})

    if request.method == 'POST':
        formset = CategoryFormset(request.POST, queryset=obj)
        if formset.is_valid():
            formset.save()

        if request.POST.get('up'):
            current_position = int(request.POST.get('up'))
            obj_before = Category.objects.get(position=current_position - 1)
            current_obj = Category.objects.get(position=current_position)
            current_obj.position = current_position - 1
            obj_before.position = current_position
            current_obj.save()
            obj_before.save()
        if request.POST.get('down'):
            current_position = int(request.POST.get('down'))
            obj_after = Category.objects.get(position=current_position + 1)
            current_obj = Category.objects.get(position=current_position)
            current_obj.position = current_position + 1
            obj_after.position = current_position
            current_obj.save()
            obj_after.save()

        if request.POST.get('delete'):
            obj = Category.objects.get(id=int(request.POST.get('delete')))
            obj.delete()
            all_obj = Category.objects.all()
            n = 1
            for i in all_obj:
                i.position = n
                n += 1
                i.save()

        if request.POST.get('add'):
            return redirect('category_setup', new=1)
        else:
            return redirect('category_setup')


def room_setup(request, new=0):
    obj = Room.objects.all()
    RoomFormset = modelformset_factory(Room, form=RoomForm, extra=new)

    if request.method == 'GET':
        formset = RoomFormset(queryset=obj)
        return render(request, 'buchungstool_settings_room_setup.html', {'room': obj, 'formset': formset})

    if request.method == 'POST':
        formset = RoomFormset(request.POST, queryset=obj)

        def number_objects():
            all_obj = Room.objects.all()
            n = 1
            for i in all_obj:
                i.position = n
                n += 1
                i.save()

        if formset.is_valid():
            formset.save()
            number_objects()

        if request.POST.get('up'):
            current_position = int(request.POST.get('up'))
            obj_before = Room.objects.get(position=current_position - 1)
            current_obj = Room.objects.get(position=current_position)
            current_obj.position = current_position - 1
            obj_before.position = current_position
            current_obj.save()
            obj_before.save()
            number_objects()
        if request.POST.get('down'):
            current_position = int(request.POST.get('down'))
            obj_after = Room.objects.get(position=current_position + 1)
            current_obj = Room.objects.get(position=current_position)
            current_obj.position = current_position + 1
            obj_after.position = current_position
            current_obj.save()
            obj_after.save()
            number_objects()
        if request.POST.get('delete'):
            obj = Room.objects.get(id=int(request.POST.get('delete')))
            obj.delete()
            number_objects()

        if request.POST.get('add'):
            return redirect('room_setup', new=1)
        else:
            return redirect('room_setup')

