from django.db import models
from django.forms import ModelForm
from django import forms
from buchungstool.models import Room


class DevicelistEntry(models.Model):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    device = models.CharField(max_length=10)
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
            'krzl',
            'behoben'
        )
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'device': forms.TextInput(attrs={'class': 'form-control'}),
            'datum': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stunde': forms.NumberInput(attrs={'class': 'form-control'}),
            'beschreibung': forms.TextInput(attrs={'class': 'form-control'}),
            'krzl': forms.TextInput(attrs={'class': 'form-control'}),
            'behoben': forms.TextInput(attrs={'class': 'form-control'}),
        }
