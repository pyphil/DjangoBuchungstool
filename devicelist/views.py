from django.shortcuts import get_object_or_404, redirect, render
from buchungstool.models import Booking
from .models import DevicelistEntry, DevicelistEntryForm, Room, DevicelistEntryFormLoggedIn, Device
from django.core.mail import send_mail


def devicelist(request, room, date, std, entry_id):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    devices = Device.objects.all()
    obj = DevicelistEntry.objects.filter(room__short_name=room)
    iPads_with_entry = []
    for i in obj:
        iPads_with_entry.append(i.device)
        print(i.device)
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
                mail_text = (
                    "Datum: " + request.POST.get('datum') + "\n" +
                    "Stunde: " + request.POST.get('stunde') + "\n" +
                    "Koffer: " + koffer.short_name + "\n" +
                    "Kürzel: " + request.POST.get('krzl') + "\n" +
                    "Beschreibung: " + request.POST.get('beschreibung')
                )
                send_mail(
                    'DjangoBuchungstool Schadenmeldung',
                    mail_text,
                    'ltests2@genm.info',
                    ['philipp.lobe@genm.info'],
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
