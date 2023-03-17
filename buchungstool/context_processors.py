from buchungstool_settings.models import Setting


def add_institution(request):
    try:
        obj = Setting.objects.get(name='settings')
        return {
            'institution_name': obj.institution,
            'institution_logo': obj.logo,
            }
    except Setting.DoesNotExist:
        return {
            'institution_name': "",
            'institution_logo': "",
            }
