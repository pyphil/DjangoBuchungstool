from django.shortcuts import get_object_or_404, redirect, render
from buchungstool.models import Booking
from .models import DevicelistEntry, DevicelistEntryForm, Room, DevicelistEntryFormLoggedIn, Device


def devicelist(request, room, date, std):
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
    }
    return render(request, 'devicelist.html', context)


def devicelistEntry(request, id, room, date, std):
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
                return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde)
        elif request.POST.get('delete'):
            obj.delete()
            return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde)
        else:
            return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde)

    context = {
        'room': room,
        'devicelist': f,
        'date': date,
        'std': std
    }

    return render(request, 'devicelistEntry.html', context)


def devicelistEntryNew(request, room, date, std):
    # get room id to pass in for initial data
    print('cancel')
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
                f.save()
                return redirect('devicelist', room=room, date=date, std=std)
        else:
            return redirect('devicelist', room=room, date=date, std=std)
    
    context = {
        'room': room,
        'devicelist': f, 
        'nodelete': True,
        'date': date,
        'std': std
    }
    
    return render(request, 'devicelistEntry.html', context)


def lastDeviceUsers(request, room, date, dev):
    # lte: less than equals
    devices = Booking.objects.filter(room=room, datum__lte=date).order_by('-datum', '-stunde')[:10]
    devlist = []
    for i in devices:
        # gettattr is equivalent to i.iPad_... and enables us to loop trough
        devlist.append({
            'datum': i.datum,
            'stunde': i.stunde,
            'krzl': i.krzl,
            'dev': getattr(i, dev),
        })
    seit_datum = date.split("-")
    seit_datum = seit_datum[2] + "." + seit_datum[1] + "." + seit_datum[0]
    return render(request, 'deviceusers.html', {'devlist': devlist, 'dev': dev, 'seit_datum': seit_datum})
