from django.shortcuts import get_object_or_404, redirect, render
from buchungstool.models import Booking, Room
from buchungstool_settings.models import Config
from .models import DevicelistEntry, DevicelistEntryForm, DevicelistEntryFormLoggedIn
from .models import Device, Status
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


def devicelist(request, room, date, std, entry_id):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    devices = Device.objects.all()
    obj = DevicelistEntry.objects.filter(room__short_name=room)
    iPads_with_entry = []
    for i in obj:
        iPads_with_entry.append(i.device)
    context = {
        'room': room,
        'date': date,
        'std': std,
        'devices': devices,
        'iPads_with_entry': iPads_with_entry,
        'devicelist': obj,
        'entry_id': entry_id,
    }
    return render(request, 'devicelist.html', context)


@login_required
def devicelist_admin(request):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    if request.GET.get('filter') and request.GET.get('filter') != "alle":
        filter = request.GET.get('filter')
        obj = DevicelistEntry.objects.filter(status__status=filter)
    else:
        obj = DevicelistEntry.objects.all()
        filter = ""

    rooms = Room.objects.filter(type='iPad')
    devices = Device.objects.all()
    iPads_with_entry = []
    for i in obj:
        iPads_with_entry.append(i.device)
    status = Status.objects.all()
    options = []
    options.append('alle')
    for s in status:
        options.append(s.status)

    context = {
        'rooms': rooms,
        'devices': devices,
        'iPads_with_entry': iPads_with_entry,
        'devicelist': obj,
        'options': options,
        'filter': filter,
    }
    return render(request, 'devicelist_admin.html', context)


def devicelistEntry(request, id, room, date, std, entry_id):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    obj = get_object_or_404(DevicelistEntry, id=id)
    if request.method == "GET":
        # Update -> load instance
        if request.user.is_authenticated:
            f = DevicelistEntryFormLoggedIn(instance=obj)
        else:
            f = DevicelistEntryForm(instance=obj)
    if request.method == "POST":
        if request.POST.get('save'):
            if request.user.is_authenticated:
                f = DevicelistEntryFormLoggedIn(request.POST, instance=obj)
            else:
                f = DevicelistEntryForm(request.POST, instance=obj)
            if f.is_valid():
                koffer = get_object_or_404(Room, id=int(request.POST.get('room')))
                device = Device.objects.get(id=int(request.POST.get('device')))
                if request.user.is_authenticated:
                    status = Status.objects.get(id=int(request.POST.get('status')))
                else:
                    status = request.POST.get('status')
                mail_text = (
                    "Datum: " + request.POST.get('datum') + "\n" +
                    "Stunde: " + request.POST.get('stunde') + "\n" +
                    "Koffer: " + koffer.short_name + "\n" +
                    "Gerät: " + str(device) + "\n" +
                    "Kürzel: " + request.POST.get('krzl') + "\n" +
                    "Beschreibung: " + request.POST.get('beschreibung') + "\n" +
                    "Status: " + str(status)
                )
                try:
                    email = Config.objects.get(name="E-Mail")
                except Config.DoesNotExist:
                    email = ""
                try:
                    noreply = Config.objects.get(name="noreply-mail")
                except Config.DoesNotExist:
                    noreply = ""
                send_mail(
                    'DjangoBuchungstool Schadenmeldung',
                    mail_text,
                    noreply,
                    [email],
                    fail_silently=True,
                )
                f.save()
                return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde, entry_id=entry_id)
        elif request.POST.get('delete'):
            obj.delete()
            return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde, entry_id=entry_id)
        else:
            return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde, entry_id=entry_id)

    context = {
        'room': room,
        'devicelist': f,
        'date': date,
        'std': std,
        'entry_id': entry_id
    }

    return render(request, 'devicelistEntry.html', context)


def devicelistEntryNew(request, room, date, std, entry_id):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    # get room id to pass in for initial data
    room_id = get_object_or_404(Room, short_name=room).id
    if request.method == "GET":
        # new empty form
        if request.user.is_authenticated:
            f = DevicelistEntryFormLoggedIn(initial={'room': room_id, 'datum': date, 'stunde': std})
        else:
            f = DevicelistEntryForm(initial={'room': room_id, 'datum': date, 'stunde': std})
    if request.method == "POST":
        if request.POST.get('save'):
            if request.user.is_authenticated:
                f = DevicelistEntryFormLoggedIn(request.POST)
            else:
                f = DevicelistEntryForm(request.POST)
            if f.is_valid():
                koffer = get_object_or_404(Room, id=int(request.POST.get('room')))
                device = Device.objects.get(id=int(request.POST.get('device')))
                if request.user.is_authenticated:
                    status = Status.objects.get(id=int(request.POST.get('status')))
                else:
                    status = request.POST.get('status')
                mail_text = (
                    "Datum: " + request.POST.get('datum') + "\n" +
                    "Stunde: " + request.POST.get('stunde') + "\n" +
                    "Koffer: " + koffer.short_name + "\n" +
                    "Gerät: " + str(device) + "\n" +
                    "Kürzel: " + request.POST.get('krzl') + "\n" +
                    "Beschreibung: " + request.POST.get('beschreibung') + "\n" +
                    "Status: " + str(status)
                )
                try:
                    email = Config.objects.get(name="E-Mail")
                except Config.DoesNotExist:
                    email = ""
                try:
                    noreply = Config.objects.get(name="noreply-mail")
                except Config.DoesNotExist:
                    noreply = ""
                send_mail(
                    'DjangoBuchungstool Schadenmeldung',
                    mail_text,
                    noreply,
                    [email],
                    fail_silently=True,
                )
                f.save()
                return redirect('devicelist', room=room, date=date, std=std, entry_id=entry_id)
        else:
            return redirect('devicelist', room=room, date=date, std=std, entry_id=entry_id)

    context = {
        'room': room,
        'devicelist': f,
        'nodelete': True,
        'date': date,
        'std': std,
        'entry_id': entry_id
    }

    return render(request, 'devicelistEntry.html', context)


def lastDeviceUsers(request, room, date, dev):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    # lte: less than equals
    devices = Booking.objects.filter(room=room, datum__lte=date).order_by('-datum', '-stunde')[:10]
    devlist = []
    for i in devices:
        print(i.datum, date)
        print(i.stunde, 1)
        # filter out current date lessons greater than current lesson
        if not (str(i.datum) == str(date) and int(i.stunde) > 1):
            # gettattr is equivalent to i.iPad_... and enables us to loop through
            devlist.append({
                'datum': i.datum,
                'stunde': i.stunde,
                'krzl': i.krzl,
                'dev': getattr(i, dev),
            })
    seit_datum = date.split("-")
    seit_datum = seit_datum[2] + "." + seit_datum[1] + "." + seit_datum[0]
    return render(request, 'deviceusers.html', {'devlist': devlist, 'dev': dev, 'seit_datum': seit_datum})
