from django.shortcuts import get_object_or_404, render
from buchungstool.models import Booking
from .models import Device, DeviceForm


def devicelist(request, room):
    print(room)
    obj = get_object_or_404(Device)
    f = DeviceForm(instance=obj)
    return render(request, 'devicelist.html', {'room': room, 'devicelist': f})


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
