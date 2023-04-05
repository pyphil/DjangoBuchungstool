from django.shortcuts import get_object_or_404, redirect, render
from buchungstool.models import Booking, Room
from buchungstool_settings.models import Config
from .models import DevicelistEntry, DevicelistEntryForm, DevicelistEntryFormLoggedIn
from .models import Device, Status
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from threading import Thread


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


def devicelist_all(request):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    if request.GET.get('filter_status') and request.GET.get('filter_status') != "alle":
        filter_status = request.GET.get('filter_status')
        obj = DevicelistEntry.objects.filter(status__status=filter_status).order_by('room', 'device')
    else:
        obj = DevicelistEntry.objects.all().order_by('room', 'device')
        filter_status = ""

    status = Status.objects.all()
    options = []
    options.append('alle')
    for s in status:
        options.append(s.status)

    context = {
        'devicelist': obj,
        'options': options,
        'filter_status': filter_status,
    }
    return render(request, 'devicelist_all.html', context)


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
                subject = 'DjangoBuchungstool Update Schadenmeldung'
                thread = MailThread(subject, mail_text, noreply, email)
                thread.start()
                f.save()
                if request.POST.get('devicelist_all'):
                    return redirect('devicelist_all')
                else:
                    return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde, entry_id=entry_id)        
            
        elif request.POST.get('delete'):
            koffer = get_object_or_404(Room, id=int(request.POST.get('room')))
            device = Device.objects.get(id=int(request.POST.get('device')))
            status = request.POST.get('status')
            if request.user.is_authenticated:
                status = Status.objects.get(id=int(request.POST.get('status')))
            else:
                status = request.POST.get('status')
            mail_text = (
                    "Folgende Schaden- oder Problemmeldung wurde gelöscht:\n\n"
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
            subject = 'DjangoBuchungstool gelöschte Schadenmeldung'
            thread = MailThread(subject, mail_text, noreply, email)
            thread.start()
            obj.delete()
            # TODO Return to devicelist_all if coming from there -> use url parameter
            if request.POST.get('devicelist_all'):
                return redirect('devicelist_all')
            else:
                return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde, entry_id=entry_id)
        else:
            return redirect('devicelist', room=obj.room, date=obj.datum, std=obj.stunde, entry_id=entry_id)

    context = {
        'room': room,
        'devicelist': f,
        'date': date,
        'std': std,
        'entry_id': entry_id,
        'devicelist_all': request.GET.get('devicelist_all'),
    }

    return render(request, 'devicelistEntry.html', context)


def devicelistEntryNew(request, room=None, date=None, std=None, entry_id=None):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    # get room id to pass in for initial data
    if room:
        room_id = get_object_or_404(Room, short_name=room).id
    else:
        room_id = None
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

                subject = 'DjangoBuchungstool Schadenmeldung'
                thread = MailThread(subject, mail_text, noreply, email)
                thread.start()

                f.save()

                if room:
                    return redirect('devicelist', room=room, date=date, std=std, entry_id=entry_id)
                else:
                    return redirect('devicelist_all')
        else:
            if room:
                return redirect('devicelist', room=room, date=date, std=std, entry_id=entry_id)
            else:
                return redirect('devicelist_all')

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


class MailThread(Thread):
    def __init__(self, subject, mail_text, noreply, email):
        super(MailThread, self).__init__()
        self.subject = subject
        self.email = email
        self.noreply = noreply
        self.mail_text = mail_text

    # run method is automatically executed on thread.start()
    def run(self):
        send_mail(
            self.subject,
            self.mail_text,
            self.noreply,
            [self.email],
            fail_silently=False,
        )
