from django.shortcuts import render, redirect
from .forms import SettingForm, InfoFrontpageForm, Setting, CategoryForm, RoomForm
from buchungstool.models import Category, Room
import os
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required


@login_required
def settings(request):
    obj, created = Setting.objects.get_or_create(name='settings')
    # If created True -> First start -> show settings
    if obj.logo:
        filepath = str(obj.logo.file)
    else:
        filepath = None
    if request.method == 'GET':
        f = SettingForm(instance=obj, label_suffix="")
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

        return redirect('buchungstoolRooms')


@login_required
def settings_frontpage_alert(request):
    obj, created = Setting.objects.get_or_create(name='settings')
    # If created True -> First start -> show settings
    if request.method == 'GET':
        f = InfoFrontpageForm(instance=obj)
        return render(request, 'buchungstool_settings_frontpage_alert.html', {'form': f})

    if request.method == 'POST':
        f = InfoFrontpageForm(request.POST, instance=obj)
        if f.is_valid():
            f.save()
        return redirect('buchungstoolRooms')


@login_required
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
            if request.POST.get('save'):
                return redirect('buchungstoolRooms')
            else:
                return redirect('category_setup')


@login_required
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
            for obj in all_obj:
                obj.position = n
                n += 1
                obj.save()

        def first_and_last_of_category():
            room_obj = Room.objects.all()
            for obj in room_obj:
                obj.is_first_of_category = False
                obj.is_last_of_category = False
                obj.save()
            for category in Category.objects.all():
                first_obj = Room.objects.filter(category=category).order_by('position').first()
                if first_obj:
                    first_obj.is_first_of_category = True
                    first_obj.save()
                last_obj = Room.objects.filter(category=category).order_by('position').last()
                if last_obj:
                    last_obj.is_last_of_category = True
                    last_obj.save()

            room_obj = Room.objects.all()    
            for obj in room_obj:
                print(obj.room, obj.category, obj.is_first_of_category, obj.is_last_of_category)

        if formset.is_valid():
            formset.save()
            number_objects()
            first_and_last_of_category()

        if request.POST.get('up'):
            current_position = int(request.POST.get('up'))
            obj_before = Room.objects.get(position=current_position - 1)
            current_obj = Room.objects.get(position=current_position)
            if obj_before.category == current_obj.category:
                current_obj.position = current_position - 1
                obj_before.position = current_position
                current_obj.save()
                obj_before.save()
                first_and_last_of_category()

        if request.POST.get('down'):
            current_position = int(request.POST.get('down'))
            obj_after = Room.objects.get(position=current_position + 1)
            current_obj = Room.objects.get(position=current_position)
            if obj_after.category == current_obj.category:
                current_obj.position = current_position + 1
                obj_after.position = current_position
                current_obj.save()
                obj_after.save()
                first_and_last_of_category()

        if request.POST.get('delete'):
            obj = Room.objects.get(id=int(request.POST.get('delete')))
            obj.delete()
            number_objects()

        if request.POST.get('add'):
            return redirect('room_setup', new=1)
        else:
            if request.POST.get('save'):
                return redirect('buchungstoolRooms')
            else:
                return redirect('room_setup')
