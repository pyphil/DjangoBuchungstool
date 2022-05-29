from django.shortcuts import get_object_or_404, render
from buchungstool.models import Booking, iPads, pens
from .models import Device, DeviceForm


def devicelist(request, room):
    print(room)
    obj = Device.objects.filter(room__short_name=room)
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


def devicelistEntry(request, room, date, dev):
    obj = Device.objects.get(room__short_name=room, krzl="MSP")
    f = DeviceForm(instance=obj)
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
