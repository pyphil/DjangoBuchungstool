from datetime import datetime
from django.shortcuts import render, redirect
from buchungstool.models import Booking
from buchungstool.models import Room
from .models import Userlist


# Create your views here.
def select(request):
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

    lists = Userlist.objects.all()

    lists_filtered = []
    for i in lists:
        print(i.datum)
        if i.datum < datetime.now().date():
            print("delete")
        elif i.datum == datetime.now().date():
            print("show")
            lists_filtered.append(i)

    return render(
        request, 'userlistSelect.html',
        {'lists': lists_filtered}
    )


def entry(request):
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

    print(request.POST.get('selection'))

    selection_query = Userlist.objects.get(
        id=request.POST.get('selection')
    )

    selection = {
        'short_name': selection_query.short_name,
        'stunde': selection_query.stunde,
        'lerngruppe': selection_query.lerngruppe
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
        save_users_query.iPad_01 = pencil + "|" + students
    if ipad == "02":
        save_users_query.iPad_02 = pencil + "|" + students
    if ipad == "03":
        save_users_query.iPad_03 = pencil + "|" + students
    if ipad == "04":
        save_users_query.iPad_04 = pencil + "|" + students
    if ipad == "05":
        save_users_query.iPad_05 = pencil + "|" + students
    if ipad == "06":
        save_users_query.iPad_06 = pencil + "|" + students
    if ipad == "07":
        save_users_query.iPad_07 = pencil + "|" + students
    if ipad == "08":
        save_users_query.iPad_08 = pencil + "|" + students
    if ipad == "09":
        save_users_query.iPad_09 = pencil + "|" + students
    if ipad == "10":
        save_users_query.iPad_10 = pencil + "|" + students
    if ipad == "11":
        save_users_query.iPad_11 = pencil + "|" + students
    if ipad == "12":
        save_users_query.iPad_12 = pencil + "|" + students
    if ipad == "13":
        save_users_query.iPad_13 = pencil + "|" + students
    if ipad == "14":
        save_users_query.iPad_14 = pencil + "|" + students
    if ipad == "15":
        save_users_query.iPad_15 = pencil + "|" + students
    if ipad == "16":
        save_users_query.iPad_16 = pencil + "|" + students

    save_users_query.save()

    return render(
        request, 'userlistSuccess.html',
        {'numbers': 0}
    )
