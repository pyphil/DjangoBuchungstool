from django.shortcuts import redirect, render
from .models import Booking
from .models import Room
from userlist.models import Userlist
import datetime


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


def home(request):
    entrydate = request.session.get('isodate')
    buttondate = request.session.get('date')
    entrystd = request.session.get('std')

    if request.POST.get('room'):
        room = request.POST.get('room')
        room_text = request.POST.get('room_text')
        request.session['room'] = room
        request.session['room_text'] = room_text
    else:
        room = request.session.get('room')
        room_text = request.session.get('room_text')

    if room is None:
        return redirect('/')

    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    if request.POST.get('submit_student'):
        ipad_text = request.POST.get('submit_student')
        ipad = ipad_text.replace(" ", "_")
        pencil = request.POST.get("pencil_"+ipad_text)
        student = request.POST.get("student_"+ipad_text).replace("|", ",")
        entry = Booking.objects.filter(
            room=room,
            datum=entrydate,
            stunde=int(entrystd)
        ).first()
        if ipad == "iPad_01":
            entry.iPad_01 = pencil + "|" + student
        if ipad == "iPad_02":
            entry.iPad_02 = pencil + "|" + student
        if ipad == "iPad_03":
            entry.iPad_03 = pencil + "|" + student
        if ipad == "iPad_04":
            entry.iPad_04 = pencil + "|" + student
        if ipad == "iPad_05":
            entry.iPad_05 = pencil + "|" + student
        if ipad == "iPad_06":
            entry.iPad_06 = pencil + "|" + student
        if ipad == "iPad_07":
            entry.iPad_07 = pencil + "|" + student
        if ipad == "iPad_08":
            entry.iPad_08 = pencil + "|" + student
        if ipad == "iPad_09":
            entry.iPad_09 = pencil + "|" + student
        if ipad == "iPad_10":
            entry.iPad_10 = pencil + "|" + student
        if ipad == "iPad_11":
            entry.iPad_11 = pencil + "|" + student
        if ipad == "iPad_12":
            entry.iPad_12 = pencil + "|" + student
        if ipad == "iPad_13":
            entry.iPad_13 = pencil + "|" + student
        if ipad == "iPad_14":
            entry.iPad_14 = pencil + "|" + student
        if ipad == "iPad_15":
            entry.iPad_15 = pencil + "|" + student
        if ipad == "iPad_16":
            entry.iPad_16 = pencil + "|" + student
        entry.save()

        state, userlist = getUserlist(room, entrydate, int(entrystd))

        return render(
            request, 'buchungstoolEntry.html',
            {
                'room': room,
                'room_text': room_text,
                'isodate': entrydate,
                'date': buttondate,
                'buttontext': request.POST.get('lerngruppe'),
                'date_series': getDateSeries(buttondate),
                'std': entrystd,
                'krzl': request.POST.get('krzl').upper()[:3],
                'userlist': userlist,
                'state': state,
                'accordion': "open"
            }
        )

    if request.POST.get('freischalten'):
        state = "off"
        if request.POST.get('freischalten') == "on":
            activate = Userlist.objects.get_or_create(
                    short_name=room,
                    datum=entrydate,
                    stunde=int(entrystd),
                    lerngruppe=request.POST.get('lerngruppe')
                )
            state = "on"
        elif request.POST.get('freischalten') == "off": 
            delete = Userlist.objects.filter(
                    short_name=room,
                    datum=entrydate,
                    stunde=int(entrystd),
                ).first()
            delete.delete()

        state, userlist = getUserlist(room, entrydate, int(entrystd))

        return render(
            request, 'buchungstoolEntry.html',
            {
                'room': room,
                'room_text': room_text,
                'isodate': entrydate,
                'date': buttondate,
                'buttontext': request.POST.get('lerngruppe'),
                'date_series': getDateSeries(buttondate),
                'std': entrystd,
                'krzl': request.POST.get('krzl').upper()[:3],
                'userlist': userlist,
                'state': state,
                'accordion': "open"
            }
        )

    if request.POST.get('save'):
        selected_date = request.POST.get('selection')
        # Prüfen ob Felder leer sind
        if request.POST.get('lerngruppe') == "" or request.POST.get('krzl') == "" or request.POST.get('lerngruppe') == " " or request.POST.get('krzl') == " ":
            return render(
                request, 'buchungstoolEntry.html',
                {
                    'room': room,
                    'room_text': room_text,
                    'isodate': entrydate,
                    'date': buttondate,
                    'buttontext': request.POST.get('lerngruppe'),
                    'date_series': getDateSeries(buttondate),
                    'std': entrystd,
                    'krzl': request.POST.get('krzl').upper()[:3],
                    'warning_empty': True,
                }
            )
        else:
            if selected_date == '0':
                # Neue Buchung für einen Termin
                new = Booking.objects.get_or_create(
                    room=room,
                    lerngruppe=request.POST.get('lerngruppe'),
                    # datum=request.POST.get('date'),
                    datum=request.session.get('isodate'),
                    stunde=entrystd,
                    krzl=request.POST.get('krzl').upper()[:3]
                )
                # new.save()
            if selected_date != '0':
                selected_series = getDateSeries(buttondate, int(selected_date))
                # Serie auf besetzte Termine testen
                # Booking.objects.filter(datum="2022-02-23").filter(stunde='6').exists()
                # .datum.isoformat().split('-')
                blocked_dates = []
                for i in selected_series:
                    d = i['date'].split('.')
                    d = d[2] + "-" + d[1] + "-" + d[0]
                    if Booking.objects.filter(room=room).filter(datum=d).filter(stunde=int(entrystd)).exists():
                        blocked_dates.append(d)

                # wenn alle frei: buchen
                if blocked_dates == []:
                    for i in selected_series:
                        d = i['date'].split('.')
                        d = d[2] + "-" + d[1] + "-" + d[0]
                        new = Booking(
                            room=room,
                            lerngruppe=request.POST.get('lerngruppe'),
                            datum=d,
                            stunde=entrystd,
                            krzl=request.POST.get('krzl').upper()[:3]
                        )
                        new.save()
                # sonst: render entry mit alert in template
                else:
                    return render(
                        request, 'buchungstoolEntry.html',
                        {
                            'room': room,
                            'room_text': room_text,
                            'isodate': entrydate,
                            'date': buttondate,
                            'buttontext': request.POST.get('lerngruppe'),
                            'std': entrystd,
                            'krzl': request.POST.get('krzl').upper()[:3],
                            'date_series': getDateSeries(buttondate),
                            'alert': True,
                            'blocked_dates': ", ".join(blocked_dates)
                        }
                    )

    if request.POST.get('cancel'):
        # render home as usual
        pass
    elif request.POST.get('deleteconfirmed'):
        entry = Booking.objects.filter(
            room=room,
            datum=entrydate,
            stunde=int(entrystd)
        ).first()
        entry.delete()
    elif request.POST.get('update'):
        entry = Booking.objects.filter(
            room=room,
            datum=entrydate,
            stunde=int(entrystd)
        ).first()
        if entry:
            # Update
            if request.POST.get('lerngruppe') != "" and request.POST.get('krzl') != "" and request.POST.get('lerngruppe') != " " and request.POST.get('krzl') != " ":
                entry.lerngruppe = request.POST.get('lerngruppe')
                entry.krzl = request.POST.get('krzl').upper()[:3]
                entry.save()
            else:
                return render(
                    request, 'buchungstoolEntry.html',
                    {
                        'room': room,
                        'room_text': room_text,
                        'isodate': entrydate,
                        'date': buttondate,
                        'buttontext': request.POST.get('lerngruppe'),
                        'std': entrystd,
                        'krzl': request.POST.get('krzl').upper()[:3],
                        'warning_empty': True,
                        'update': True
                    }
                )

    direction = None
    if request.POST.get('direction'):
        direction = request.POST.get('direction')
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
                        'lerngruppe': dbobject.lerngruppe,
                        'date': date,
                        'std': std,
                        'krzl': dbobject.krzl
                    }
                )
            else:
                btncontent.append(["frei", date, std])
                btncontent.append(
                    {'lerngruppe': "frei", 'date': date, 'std': std})

    if request.POST.get('delete'):
        return render(
            request, 'buchungstoolConfirmation.html',
            {'date': entrydate, 'lerngruppe': request.POST.get('lerngruppe'),
                'std': entrystd, 'room': room, 'room_text': room_text,
                'buttondate': buttondate, 'krzl': request.POST.get('krzl').upper()[:3]}
        )
    else:
        response = render(
            request, 'buchungstoolHome.html',
            {
                'room': room,
                'room_text': room_text,
                'dates': dates,
                'btncontent': btncontent,
                'currentdate': currentdate
            }
        )
        response.set_cookie('offset', offset)
        return response


def eintrag(request):
    # room = request.POST.get('room')
    # room_text = request.POST.get('room_text')
    room = request.session.get('room')
    room_text = request.session.get('room_text')

    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    buttontext = request.POST.get('buttontext')
    krzl = request.POST.get('buttonkrzl')
    std = request.POST.get('buttonstd')

    request.session['buttontext'] = buttontext
    request.session['krzl'] = krzl
    request.session['std'] = std

    isodate = request.POST.get('button_isodate')
    date = request.POST.get('button_date')
    request.session['isodate'] = isodate
    request.session['date'] = date

    if buttontext == "frei":
        buttontext = ""
        state = None
        userlist = None
    else:
        state, userlist = getUserlist(room, isodate, std)

    date_series = getDateSeries(date)
    return render(
        request, 'buchungstoolEntry.html',
        {
            'room': room,
            'room_text': room_text,
            'isodate': isodate,
            'date': date,
            'buttontext': buttontext,
            'std': std,
            'krzl': krzl,
            'date_series': date_series,
            'userlist': userlist,
            'state': state,
            'accordion': "closed"
        }
    )


def getWeekCalendar(request, direction=None):
    try:
        offset = int(request.COOKIES['offset'])
    except Exception:
        pass

    if request.POST.get('currentdate'):
        currentdate = request.POST.get('currentdate')
        currentdate = datetime.datetime.strptime(currentdate, '%Y-%m-%d')
        currentdate = currentdate.date()
        offset = 0
        print("currentdate")
    elif request.POST.get('currentdate_nav'):
        currentdate = request.POST.get('currentdate_nav')
        currentdate = datetime.datetime.strptime(currentdate, '%Y-%m-%d')
        currentdate = currentdate.date()
        print("nav")
    elif request.POST.get('date'):
        offset = 0
        currentdate = request.POST.get('date')
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

    date = datetime.datetime.strptime(date, '%d.%m.%Y')

    date_series = []
    date_series.append({'date': date.strftime('%d.%m.%Y'), 'item': 0})
    for i in range(end):
        date = date + datetime.timedelta(days=7)
        date_series.append(
            {'date': date.strftime('%d.%m.%Y'), 'item': i + 1}
        )

    return date_series

def getUserlist(room, isodate, std):
    userlist = []

    dbobject = Booking.objects.filter(
            room=room,
            datum=isodate,
            stunde=std
    ).first()
    n = dbobject.iPad_01.split("|")
    userlist.append({'iPad': "iPad 01", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_02.split("|")
    userlist.append({'iPad': "iPad 02", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_03.split("|")
    userlist.append({'iPad': "iPad 03", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_04.split("|")
    userlist.append({'iPad': "iPad 04", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_05.split("|")
    userlist.append({'iPad': "iPad 05", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_06.split("|")
    userlist.append({'iPad': "iPad 06", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_07.split("|")
    userlist.append({'iPad': "iPad 07", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_08.split("|")
    userlist.append({'iPad': "iPad 08", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_09.split("|")
    userlist.append({'iPad': "iPad 09", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_10.split("|")
    userlist.append({'iPad': "iPad 10", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_11.split("|")
    userlist.append({'iPad': "iPad 11", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_12.split("|")
    userlist.append({'iPad': "iPad 12", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_13.split("|")
    userlist.append({'iPad': "iPad 13", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_14.split("|")
    userlist.append({'iPad': "iPad 14", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_15.split("|")
    userlist.append({'iPad': "iPad 15", 'pencil': n[0], 'student': n[1]})
    n = dbobject.iPad_16.split("|")
    userlist.append({'iPad': "iPad 16", 'pencil': n[0], 'student': n[1]})

    activated = Userlist.objects.filter(
        short_name=dbobject.room,
        datum=isodate,
        stunde=std
    ).first()

    if activated:
        return "on", userlist
    else:
        return "off", userlist