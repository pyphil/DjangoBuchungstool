from django.shortcuts import render
from buchungstool.models import Booking


def devicelist(request):
    devices = Booking.objects.filter(room="M-A").order_by('-datum', '-stunde')[:10]
    return render(request, 'devicelist.html', {'devices': devices})
