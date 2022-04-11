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

    return render(
        request, 'userlistSelect.html',
        {'lists': lists}
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

    selection_query = Userlist.objects.filter(
        short_name=request.POST.get('selection')
    ).first()

    selection = {
        'short_name': request.POST.get('selection'),
        # 'datum': selection_query.datum,
        # 'stunde': selection_query.stunde
    }
    request.session['short_name'] = request.POST.get('selection')
    # request.session['datum'] = str(selection_query.datum)
    # request.session['stunde'] = selection_query.stunde

    numbers = [""]
    for i in range(1, 17):
        numbers.append(("%02d" % i))

    return render(
        request, 'userlistEntry.html',
        {'numbers': numbers, }
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

    print(request.POST.get('iPad'))
    print(request.POST.get('pencil'))
    print(request.POST.get('students'))

    # print(request.session.get('short_name'))
    # print(request.session.get('datum'))
    # print(request.session.get('stunde'))


    return render(
        request, 'userlistSuccess.html',
        {'numbers': 0}
    )
