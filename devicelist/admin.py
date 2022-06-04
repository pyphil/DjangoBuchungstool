from django.contrib import admin
from .models import DevicelistEntry
from .models import Device


class DeviceCustomAdmin(admin.ModelAdmin):
    list_display = (
        'device', 'room', 'datum', 'stunde', 'beschreibung', 'krzl', 'behoben',
    )
    list_filter = (
        'device', 'room', 'datum', 'stunde', 'beschreibung', 'krzl', 'behoben',
    )


admin.site.register(DevicelistEntry, DeviceCustomAdmin)
admin.site.register(Device)
