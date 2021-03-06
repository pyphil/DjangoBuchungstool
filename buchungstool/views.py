from django.shortcuts import redirect, render, get_object_or_404
from .models import Booking, Room, BookingFormIpad
from userlist.models import Userlist
import datetime
from django.core.mail import send_mail


def rooms(request):
    # Zugriff nur mit access key in production
    if not request.session.get('has_access'):
        try:
            from .production_access import ACCESSKEY
        except ImportError:
            # development
            request.session['has_access'] = True
        else:
            if request.GET.get('access') != ACCESSKEY:
                return render(request, 'buchungstoolNoAccess.html')
            else:
                request.session['has_access'] = True
                return redirect('/')
    elif request.GET.get('access') and request.session.get('has_access'):
        return redirect('/')

    rooms = Room.objects.all()

    return render(
        request, 'buchungstoolRooms.html',
        {'rooms': rooms}
    )


def home(request, room=None):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    if room:
        print(room)
        room_obj = get_object_or_404(Room, short_name=room)
        print(room_obj.room, room_obj.description)

    if room is None:
        return redirect('/')

    direction = None
    if request.GET.get('direction'):
        direction = request.GET.get('direction')
    dates, offset, currentdate = getWeekCalendar(request, direction)
    currentdate = currentdate.strftime('%Y-%m-%d')

    btncontent = []

    for std in [1, 2, 3, 4, 5, 6, 7]:
        for date in dates:
            dbobject = Booking.objects.filter(
                room=room,
                datum=date['isodate'],
                stunde=std
            ).first()
            if dbobject:
                btncontent.append(
                    {
                        'id': dbobject.id,
                        'lerngruppe': dbobject.lerngruppe,
                        'date': date,
                        'std': std,
                        'krzl': dbobject.krzl
                    }
                )
            else:
                btncontent.append(["frei", date, std])
                btncontent.append(
                    {'id': 0, 'lerngruppe': "frei", 'date': date, 'std': std})

    response = render(
        request, 'buchungstoolHome.html',
        {
            'room': room_obj.short_name,
            'room_text': room_obj.room + " - " + room_obj.description,
            'room_alert': room_obj.alert,
            'dates': dates,
            'btncontent': btncontent,
            'currentdate': currentdate
        }
    )
    response.set_cookie('offset', offset)
    return response


def eintrag(request, accordion=None, room=None, id=None):
    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    if accordion or request.GET.get('accordion'):
        accordion = "open"
    else:
        accordion = "closed"

    if request.POST.get('reload'):
        return redirect('/buchungstool/' + room + "/" + str(id) + '/?accordion="open"#userlist')

    room_obj = Room.objects.get(short_name=room)

    if id != 0:
        entry_obj = get_object_or_404(Booking, id=id)
        isodate = str(entry_obj.datum)
        date = entry_obj.datum.strftime('%d.%m.%Y')
        lerngruppe = entry_obj.lerngruppe
        std = entry_obj.stunde
        krzl = entry_obj.krzl

        state, userlist = getUserlist(room, isodate, std)
        initial_list = []
        for i in userlist:
            initial_list.append(i.value())
        request.session['initial_list'] = initial_list
    elif id == 0:
        # neuer Eintrag Variablen vorbereiten
        isodate = request.GET.get('isodate')
        date = datetime.datetime.strptime(isodate, '%Y-%m-%d').strftime('%d.%m.%Y')
        std = request.GET.get('std')
        lerngruppe = ""
        krzl = ""
        state = None
        userlist = None

    if request.POST.get('submit_student'):
        f = BookingFormIpad(request.POST, instance=entry_obj)

        z = 0
        changed_fields = []
        for i in f:
            if i.value() != request.session.get('initial_list')[z]:
                changed_fields.append(i.name)
            z += 1
        del request.session['initial_list']
        obj = f.save(commit=False)
        obj.save(update_fields=changed_fields)

        return redirect('/buchungstool/' + room + "/" + str(id) + '/?accordion="open"#userlist')

    if request.POST.get('freischalten'):
        state = "off"
        if request.POST.get('freischalten') == "on":
            Userlist.objects.get_or_create(
                short_name=room,
                datum=isodate,
                stunde=std,
                lerngruppe=lerngruppe,
                krzl=krzl,
                created=datetime.datetime.now()
            )
            state = "on"
        elif request.POST.get('freischalten') == "off":
            delete = Userlist.objects.get(
                short_name=room,
                datum=isodate,
                stunde=std,
            )
            delete.delete()

        return redirect('/buchungstool/' + room + "/" + str(id) + '/?accordion="open"#userlist')

    warning = False
    alert = False
    blocked_dates = None

    if request.POST.get('save'):
        selected_date = request.POST.get('selection')
        # Pr??fen ob Felder leer sind
        if request.POST.get('lerngruppe') == "" or request.POST.get('krzl') == "" or request.POST.get('lerngruppe') == " " or request.POST.get('krzl') == " ":
            warning = True
        else:
            if selected_date == '0':
                # Neue Buchung f??r einen Termin
                new = Booking.objects.get_or_create(
                    room=room,
                    lerngruppe=request.POST.get('lerngruppe'),
                    datum=isodate,
                    stunde=std,
                    krzl=request.POST.get('krzl').upper()[:3]
                )
                return redirect('/buchungstool/' + room + '/?date=' + isodate)
            if selected_date != '0':
                selected_series = getDateSeries(isodate, int(selected_date))
                # Serie auf besetzte Termine testen
                # Booking.objects.filter(datum="2022-02-23").filter(stunde='6').exists()
                # .datum.isoformat().split('-')
                blocked_dates = []
                for i in selected_series:
                    d = i['date'].split('.')
                    d = d[2] + "-" + d[1] + "-" + d[0]
                    if Booking.objects.filter(room=room).filter(datum=d).filter(stunde=std).exists():
                        blocked_dates.append(d)

                # wenn alle frei: einen oder alle buchen
                if blocked_dates == []:
                    for i in selected_series:
                        d = i['date'].split('.')
                        d = d[2] + "-" + d[1] + "-" + d[0]
                        new = Booking(
                            room=room,
                            lerngruppe=request.POST.get('lerngruppe'),
                            datum=d,
                            stunde=std,
                            krzl=request.POST.get('krzl').upper()[:3]
                        )
                        new.save()
                    return redirect('/buchungstool/' + room + '/?date=' + isodate)
                # sonst: render entry mit alert in template
                else:
                    alert = True

    update = False

    if request.POST.get('update'):
        if request.POST.get('lerngruppe') == "" or request.POST.get('krzl') == "" or request.POST.get('lerngruppe') == " " or request.POST.get('krzl') == " ":
            warning = True
            update = True
        else:
            entry_obj.lerngruppe = request.POST.get('lerngruppe')
            entry_obj.krzl = request.POST.get('krzl').upper()[:3]
            entry_obj.save()
            print('update')
            return redirect('/buchungstool/' + room + '/?date=' + isodate)

    if request.POST.get('cancel'):
        # redirect to home
        return redirect('/buchungstool/' + room + '/?date=' + isodate)

    if request.POST.get('delete'):
        context = {
            'date': isodate,
            'lerngruppe': lerngruppe,
            'std': std,
            'room': room,
            'buttondate': date,
            'krzl': krzl,
            'id': id
        }
        return render(request, 'buchungstoolConfirmation.html', context)

    if request.POST.get('deleteconfirmed'):
        entry_obj.delete()
        delete_userlist_entry = Userlist.objects.filter(
            short_name=room,
            datum=isodate,
            stunde=std,
        ).first()
        if delete_userlist_entry:
            delete_userlist_entry.delete()
        return redirect('/buchungstool/' + room + '/?date=' + isodate)

    date_series = getDateSeries(isodate)

    return render(
        request, 'buchungstoolEntry.html',
        {
            'room': room,
            'room_text': room_obj.room + " - " + room_obj.description,
            'isodate': isodate,
            'date': date,
            'buttontext': lerngruppe,
            'std': std,
            'krzl': krzl,
            'date_series': date_series,
            'userlist': userlist,
            'state': state,
            'accordion': accordion,
            'warning_empty': warning,
            'update': update,
            'alert': alert,
            'blocked_dates': blocked_dates,
            'entry_id': id
        }
    )


def getWeekCalendar(request, direction=None):
    try:
        offset = int(request.COOKIES['offset'])
    except Exception:
        pass

    if request.GET.get('currentdate'):
        currentdate = request.GET.get('currentdate')
        currentdate = datetime.datetime.strptime(currentdate, '%Y-%m-%d')
        currentdate = currentdate.date()
        offset = 0
        print("currentdate")
    elif request.GET.get('currentdate_nav'):
        currentdate = request.GET.get('currentdate_nav')
        currentdate = datetime.datetime.strptime(currentdate, '%Y-%m-%d')
        currentdate = currentdate.date()
        print("nav")
    elif request.GET.get('date'):
        offset = 0
        currentdate = request.GET.get('date')
        currentdate = datetime.datetime.strptime(currentdate, '%Y-%m-%d')
        currentdate = currentdate.date()
        print("date")
    else:
        currentdate = datetime.date.today()
        offset = 0
        print("today")

    # Starts with knowing the day of the week
    # .weekday statt [2] funktioniert erst ab Python 3.9
    week_day = currentdate.isocalendar()[2]

    if direction == "forward":
        offset = offset + 7
    if direction == "back":
        offset = offset - 7

    # Calculates Starting date for this case by subtracting current date with
    # time delta of the day of the week
    start_date = currentdate - datetime.timedelta(days=week_day)
    start_date = start_date + datetime.timedelta(days=offset)

    # Prints the list of dates in a current week
    # weekdays = ["Mo, ", "Di, ", "Mi, ", "Do, ", "Fr, ", "Sa, ", "So, "]
    weekdays = ["Mo, ", "Di, ", "Mi, ", "Do, ", "Fr, "]
    dates = []
    i = 1
    for day in weekdays:
        isodate = (start_date + datetime.timedelta(days=i)).isoformat()

        dates.append(
            {"weekday": day, "date": datetime.datetime.strptime(
                isodate, '%Y-%m-%d').strftime('%d.%m.%Y'),
                "isodate": str(isodate)
             }
        )
        i += 1

    return dates, offset, currentdate


def getDateSeries(date, end=None):
    if end is None:
        end = 24

    date = datetime.datetime.strptime(date, '%Y-%m-%d')

    date_series = []
    date_series.append({'date': date.strftime('%d.%m.%Y'), 'item': 0})
    for i in range(end):
        date = date + datetime.timedelta(days=7)
        date_series.append(
            {'date': date.strftime('%d.%m.%Y'), 'item': i + 1}
        )

    return date_series


def getUserlist(room, isodate, std):
    # userlist = []

    dbobject = Booking.objects.get(
        room=room,
        datum=isodate,
        stunde=std
    )

    f = BookingFormIpad(instance=dbobject)

    # delete objects that are more than 20 min old
    lists = Userlist.objects.all()
    for i in lists:
        diff = datetime.datetime.now() - i.created.replace(tzinfo=None)
        if diff.total_seconds()/60 > 20:
            i.delete()

    activated = Userlist.objects.filter(
        short_name=dbobject.room,
        datum=isodate,
        stunde=std
    ).exists()

    if activated:
        return "on", f
    else:
        return "off", f


def userlistInfo(request):

    send_mail(
        'DjangoBuchungstool Message',
        'Info has been clicked.',
        'ltests2@genm.info',
        ['philipp.lobe@genm.info'],
        fail_silently=True,
    )

    return render(request, 'buchungstoolUserlistInfo.html', {})
