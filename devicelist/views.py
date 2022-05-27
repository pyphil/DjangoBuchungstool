from django.shortcuts import render
from buchungstool.models import Booking


def devicelist(request, room, date, dev):
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

    return render(request, 'devicelist.html', {'devlist': devlist, 'dev': dev})
