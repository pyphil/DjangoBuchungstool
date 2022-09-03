from django.db import models
from django.forms import ModelForm
from django import forms
from buchungstool.models import Room


class Device(models.Model):
    device = models.CharField(max_length=10)
    dbname = models.CharField(max_length=10)

    def __str__(self):
        return self.device


class Status(models.Model):
    status = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Status"


class DevicelistEntry(models.Model):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    # device = models.CharField(max_length=10)
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    datum = models.DateField()
    stunde = models.IntegerField()
    beschreibung = models.CharField(max_length=300)
    krzl = models.CharField(max_length=10)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, default=1)
    behoben = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name_plural = "DevicelistEntries"


class DevicelistEntryForm(ModelForm):
    class Meta:
        model = DevicelistEntry
        fields = (
            'room',
            'device',
            'datum',
            'stunde',
            'beschreibung',
            'krzl'
        )
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'device': forms.Select(attrs={'class': 'form-select'}),
            'datum': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stunde': forms.NumberInput(attrs={'class': 'form-control'}),
            'beschreibung': forms.TextInput(attrs={'class': 'form-control'}),
            'krzl': forms.TextInput(attrs={'class': 'form-control'})
        }


class DevicelistEntryFormLoggedIn(ModelForm):
    class Meta:
        model = DevicelistEntry
        fields = (
            'room',
            'device',
            'datum',
            'stunde',
            'beschreibung',
            'krzl',
            'status',
            'behoben'
        )
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'device': forms.Select(attrs={'class': 'form-select'}),
            'datum': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stunde': forms.NumberInput(attrs={'class': 'form-control'}),
            'beschreibung': forms.TextInput(attrs={'class': 'form-control'}),
            'krzl': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'behoben': forms.TextInput(attrs={'class': 'form-control'}),
        }
