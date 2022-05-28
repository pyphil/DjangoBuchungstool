from django.db import models
from django.forms import ModelForm
from buchungstool.models import Room


class Device(models.Model):
    room = models.ForeignKey(Room, blank=True, on_delete=models.DO_NOTHING)
    device = models.CharField(max_length=10)
    datum = models.DateField()
    stunde = models.IntegerField()
    beschreibung = models.CharField(max_length=300)
    krzl = models.CharField(max_length=10)
    behoben = models.CharField(max_length=10, blank=True)


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = [
            'device',
            'datum',
            'stunde',
            'beschreibung',
            'krzl',
            'behoben'
        ]
