from django.db import models
from django.forms import ModelForm
from django import forms
from buchungstool.models import Room


class Device(models.Model):
    device = models.CharField(max_length=10)
    dbname = models.CharField(max_length=10)

    def __str__(self):
        return self.device


class DevicelistEntry(models.Model):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    # device = models.CharField(max_length=10)
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    datum = models.DateField()
    stunde = models.IntegerField()
    beschreibung = models.CharField(max_length=300)
    krzl = models.CharField(max_length=10)
    behoben = models.CharField(max_length=10, blank=True)


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
            'behoben'
        )
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'device': forms.Select(attrs={'class': 'form-select'}),
            'datum': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stunde': forms.NumberInput(attrs={'class': 'form-control'}),
            'beschreibung': forms.TextInput(attrs={'class': 'form-control'}),
            'krzl': forms.TextInput(attrs={'class': 'form-control'}),
            'behoben': forms.TextInput(attrs={'class': 'form-control'}),
        }
