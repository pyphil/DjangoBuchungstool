from django.shortcuts import get_object_or_404, redirect, render
from buchungstool.models import Booking, iPads, pens
from .models import DevicelistEntry, DevicelistEntryForm


def devicelist(request, room):
    print(room)
    obj = DevicelistEntry.objects.filter(room__short_name=room)
    iPads_with_entry = []
    for i in obj:
        iPads_with_entry.append(i.device)
    context = {
        'room': room,
        'iPads': iPads,
        'pens': pens,
        'iPads_with_entry': iPads_with_entry,
        'devicelist': obj,
    }
    return render(request, 'devicelist.html', context)


def devicelistEntry(request, room, date, std, dev):
    if request.method == "GET":
            # Update -> load instance
            obj = DevicelistEntry.objects.get(room__short_name=room, datum=date, stunde=std, device=dev)
            f = DevicelistEntryForm(instance=obj)
    if request.method == "POST":
        f = DevicelistEntryForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('/devices/' + room + "/")
    dev = dev.replace("_", " ")
    return render(request, 'devicelistEntry.html', {'room': room, 'dev': dev, 'devicelist': f})


def devicelistEntryNew(request, room, date, std):
    if request.method == "GET":
        # new empty form
        # TODO: Pass in the id of room
        f = DevicelistEntryForm(initial={'room': room, 'datum': date, 'stunde': std})
    if request.method == "POST":
        f = DevicelistEntryForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('/devices/' + room + "/")
    return render(request, 'devicelistEntry.html', {'room': room, 'devicelist': f})


def lastDeviceUsers(request, room, date, dev):
    print(dev)
    devices = Booking.objects.filter(room=room, datum__lte=date).order_by('-datum', '-stunde')[:50]
    devlist = []
    for i in devices:
        print(i.datum)
        print(i.stunde)
        print(i.krzl)
        # gettattr is equivalent to i.iPad_...
        print(getattr(i, dev))
        devlist.append({
            'datum': i.datum,
            'stunde': i.stunde,
            'krzl': i.krzl,
            'dev': getattr(i, dev),
        })

    return render(request, 'deviceusers.html', {'devlist': devlist, 'dev': dev})
