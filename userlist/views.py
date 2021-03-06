from datetime import datetime
from django.shortcuts import render, redirect
from buchungstool.models import Booking
from .models import Userlist


def select(request):
    # Zugriff nur mit access key in production
    if not request.session.get('student_access'):
        try:
            from .production_access import ACCESSKEY
        except ImportError:
            # development
            request.session['student_access'] = True
        else:
            if request.GET.get('access') != ACCESSKEY:
                return render(request, 'buchungstoolNoAccess.html')
            else:
                request.session['student_access'] = True
                return redirect('/userlist/select/')
    elif request.GET.get('access') and request.session.get('student_access'):
        return redirect('/userlist/select/')

    # delete objects that are more than 20 min old
    lists = Userlist.objects.all()
    for i in lists:
        diff = datetime.now() - i.created.replace(tzinfo=None)
        if diff.total_seconds()/60 > 20:
            i.delete()

    # only show objects made for today's date
    lists = Userlist.objects.filter(
        datum=datetime.now().date()
    )

    return render(
        request, 'userlistSelect.html',
        {'lists': lists}
    )


def entry(request):
    # Zugriff nur mit access key in production
    if not request.session.get('student_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    selection_query = Userlist.objects.get(
        id=request.POST.get('selection')
    )

    selection = {
        'short_name': selection_query.short_name,
        'stunde': selection_query.stunde,
        'lerngruppe': selection_query.lerngruppe,
        'krzl': selection_query.krzl

    }
    request.session['id'] = request.POST.get('selection')

    numbers = [""]
    for i in range(1, 17):
        numbers.append(("%02d" % i))

    return render(
        request, 'userlistEntry.html',
        {'numbers': numbers, 'selection': selection}
    )


def success(request):
    # Zugriff nur mit access key in production
    if not request.session.get('student_access'):
        return render(request, 'buchungstoolNoAccess.html',)

    ipad = request.POST.get('iPad')
    pencil = request.POST.get('pencil')
    students = request.POST.get('students')

    selection_query = Userlist.objects.get(
            id=request.session.get('id')
    )

    save_users_query = Booking.objects.filter(
        room=selection_query.short_name,
        datum=selection_query.datum,
        stunde=selection_query.stunde,
    ).first()

    if ipad == "01":
        save_users_query.iPad_01 = students
        save_users_query.pen_01 = pencil
    if ipad == "02":
        save_users_query.iPad_02 = students
        save_users_query.pen_02 = pencil
    if ipad == "03":
        save_users_query.iPad_03 = students
        save_users_query.pen_03 = pencil
    if ipad == "04":
        save_users_query.iPad_04 = students
        save_users_query.pen_04 = pencil
    if ipad == "05":
        save_users_query.iPad_05 = students
        save_users_query.pen_05 = pencil
    if ipad == "06":
        save_users_query.iPad_06 = students
        save_users_query.pen_06 = pencil
    if ipad == "07":
        save_users_query.iPad_07 = students
        save_users_query.pen_07 = pencil
    if ipad == "08":
        save_users_query.iPad_08 = students
        save_users_query.pen_08 = pencil
    if ipad == "09":
        save_users_query.iPad_09 = students
        save_users_query.pen_09 = pencil
    if ipad == "10":
        save_users_query.iPad_10 = students
        save_users_query.pen_10 = pencil
    if ipad == "11":
        save_users_query.iPad_11 = students
        save_users_query.pen_11 = pencil
    if ipad == "12":
        save_users_query.iPad_12 = students
        save_users_query.pen_12 = pencil
    if ipad == "13":
        save_users_query.iPad_13 = students
        save_users_query.pen_13 = pencil
    if ipad == "14":
        save_users_query.iPad_14 = students
        save_users_query.pen_14 = pencil
    if ipad == "15":
        save_users_query.iPad_15 = students
        save_users_query.pen_15 = pencil
    if ipad == "16":
        save_users_query.iPad_16 = students
        save_users_query.pen_16 = pencil

    save_users_query.save()

    return render(
        request, 'userlistSuccess.html',
        {'numbers': 0}
    )
