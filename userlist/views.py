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

    numbers = []
    for i in range(1,17):
        numbers.append(("%02d" % i))
    
    

    return render(
        request, 'userlistEntry.html',
        {'numbers': numbers}
    )