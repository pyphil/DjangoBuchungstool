from django.db import models
from django.forms import ModelForm
from django import forms
from buchungstool.models import Room


class Device(models.Model):
    def get_next_number():
        """
        Returns the next integer value in the dataset.
        """
        devices = Device.objects.all()
        if devices.count() == 0:
            return 1
        else:
            return devices.aggregate(models.Max('position'))['position__max'] + 1
    device = models.CharField(max_length=30)
    dbname = models.CharField(max_length=10, blank=True, null=True)
    position = models.PositiveIntegerField(default=get_next_number)

    def __str__(self):
        return self.device

    class Meta:
        ordering = ['position']


class Status(models.Model):
    status = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Status"


class DevicelistEntry(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
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

    @property
    def age(self):
        from datetime import date
        today = date.today()
        age = today - self.datum
        age = str(age).split('d')[0].strip()
        return age


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
            'datum': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'style': "height: 38px;"}),
            'stunde': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 11}),
            'beschreibung': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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
            'datum': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'style': "height: 38px;"}),
            'stunde': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 11}),
            'beschreibung': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'krzl': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'behoben': forms.TextInput(attrs={'class': 'form-control'}),
        }
