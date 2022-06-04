from django.shortcuts import get_object_or_404, redirect, render
from buchungstool.models import Booking, iPads, pens
from .models import DevicelistEntry, DevicelistEntryForm, Room


def devicelist(request, room, date, std):
    obj = DevicelistEntry.objects.filter(room__short_name=room)
    iPads_with_entry = []
    for i in obj:
        iPads_with_entry.append(i.device)
    context = {
        'room': room,
        'datum': date,
        'stunde': std,
        'iPads': iPads,
        'pens': pens,
        'iPads_with_entry': iPads_with_entry,
        'devicelist': obj,
    }
    return render(request, 'devicelist.html', context)


def devicelistEntry(request, id):
    obj = get_object_or_404(DevicelistEntry, id=id)
    if request.method == "GET":
        # Update -> load instance
        f = DevicelistEntryForm(instance=obj)
    if request.method == "POST":
        f = DevicelistEntryForm(request.POST, instance=obj)
        if f.is_valid():
            f.save()
            # return redirect('/devices/' + str(obj.room) + "/")
            return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde)
    dev = obj.device
    dev = dev.replace("_", " ")
    return render(request, 'devicelistEntry.html', {'room': obj.room, 'dev': dev, 'devicelist': f})


def devicelistEntryNew(request, room, date, std):
    # get room id to pass in for initial data
    room_id = get_object_or_404(Room, short_name=room).id
    print(room_id)
    if request.method == "GET":
        # new empty form
        f = DevicelistEntryForm(initial={'room': room_id, 'datum': date, 'stunde': std})
    if request.method == "POST":
        f = DevicelistEntryForm(request.POST)
        if f.is_valid():
            f.save()
            # return redirect('/devices/' + room + "/" + date + "/" + str(std) + "/")
            return redirect('devicelist', room=room, date=date, std=std)
    return render(request, 'devicelistEntry.html', {'room': room, 'devicelist': f})


def lastDeviceUsers(request, room, date, dev):
    print(dev)
    devices = Booking.objects.filter(room=room, datum__lte=date).order_by('-datum', '-stunde')[:10]
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
    seit_datum = date.split("-")
    seit_datum = seit_datum[2] + "." + seit_datum[1] + "." + seit_datum[0]
    return render(request, 'deviceusers.html', {'devlist': devlist, 'dev': dev, 'seit_datum': seit_datum})
