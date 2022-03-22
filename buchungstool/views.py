from django.shortcuts import redirect, render
from .models import Booking
from .models import Room
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
    entrydate = request.POST.get('date')
    buttondate = request.POST.get('buttondate')
    entrystd = request.POST.get('std')
    room = request.POST.get('room')
    room_text = request.POST.get('room_text')
    
    if room is None:
        return redirect('/')

    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    if request.POST.get('save'):
        selected_date = request.POST.get('selection')
        if selected_date == '0':
            print("nur einen Termin buchen")
            # Neue Buchung
            new = Booking(
                room=room,
                lerngruppe=request.POST.get('lerngruppe'),
                datum=request.POST.get('date'),
                stunde=entrystd,
                krzl=request.POST.get('krzl').upper()[:3]
            )
            new.save()
        if selected_date != '0':
            selected_series = getDateSeries(buttondate, int(selected_date))
            # Serie auf besetzte Termine testen
            # Booking.objects.filter(datum="2022-02-23").filter(stunde='6').exists()
            # .datum.isoformat().split('-')
            blocked_dates = []
            for i in selected_series:
                d = i['date'].split('.')
                d = d[2] + "-" + d[1] + "-" + d[0]
                print(d)
                if Booking.objects.filter(room=room).filter(datum=d).filter(stunde=int(entrystd)).exists():
                    blocked_dates.append(d)

            # wenn alle frei: buchen
            if blocked_dates == []:
                print("buchen")
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
                print("folgende Termine sind besetzt:")
                for i in blocked_dates:
                    print(i)
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
            entry.lerngruppe = request.POST.get('lerngruppe')
            entry.krzl = request.POST.get('krzl').upper()[:3]
            entry.save()

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
                'buttondate': buttondate}
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
    room = request.POST.get('room')
    room_text = request.POST.get('room_text')

    if not request.session.get('has_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    buttontext = request.POST.get('buttontext')
    krzl = request.POST.get('buttonkrzl')
    std = request.POST.get('buttonstd')

    if buttontext == "frei":
        buttontext = ""

    isodate = request.POST.get('button_isodate')
    date = request.POST.get('button_date')
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
            'date_series': date_series
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
    elif request.POST.get('currentdate_nav'):
        currentdate = request.POST.get('currentdate_nav')
        currentdate = datetime.datetime.strptime(currentdate, '%Y-%m-%d')
        currentdate = currentdate.date()
    elif request.POST.get('date'):
        offset = 0
        currentdate = request.POST.get('date')
        currentdate = datetime.datetime.strptime(currentdate, '%Y-%m-%d')
        currentdate = currentdate.date()
    else:
        currentdate = datetime.date.today()
        offset = 0

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
