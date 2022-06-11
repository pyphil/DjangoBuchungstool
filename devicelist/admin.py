from django.contrib import admin
from .models import DevicelistEntry
from .models import Device
from .models import Status


class DeviceCustomAdmin(admin.ModelAdmin):
    list_display = (
        'device', 'room', 'datum', 'stunde', 'beschreibung', 'krzl', 'status', 'behoben',
    )
    list_filter = (
        'device', 'room', 'datum', 'stunde', 'beschreibung', 'krzl', 'status', 'behoben',
    )


class StatusCustomAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'color')


admin.site.register(DevicelistEntry, DeviceCustomAdmin)
admin.site.register(Device)
admin.site.register(Status, StatusCustomAdmin)
