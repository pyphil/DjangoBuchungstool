from buchungstool_settings.models import Setting


def add_institution(request):
    obj = Setting.objects.get(name='settings')
    return {
        'institution_name': obj.institution,
        'institution_logo': obj.logo,
        }
