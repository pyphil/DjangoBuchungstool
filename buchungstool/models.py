from django.db import models
from ckeditor.fields import RichTextField
from django import forms
from django.forms import ModelForm


class Booking(models.Model):
    room = models.CharField(max_length=10)
    krzl = models.CharField(max_length=3)
    lerngruppe = models.CharField(max_length=30)
    datum = models.DateField()
    stunde = models.IntegerField()
    iPad_01 = models.CharField(max_length=40, blank=True)
    iPad_02 = models.CharField(max_length=40, blank=True)
    iPad_03 = models.CharField(max_length=40, blank=True)
    iPad_04 = models.CharField(max_length=40, blank=True)
    iPad_05 = models.CharField(max_length=40, blank=True)
    iPad_06 = models.CharField(max_length=40, blank=True)
    iPad_07 = models.CharField(max_length=40, blank=True)
    iPad_08 = models.CharField(max_length=40, blank=True)
    iPad_09 = models.CharField(max_length=40, blank=True)
    iPad_10 = models.CharField(max_length=40, blank=True)
    iPad_11 = models.CharField(max_length=40, blank=True)
    iPad_12 = models.CharField(max_length=40, blank=True)
    iPad_13 = models.CharField(max_length=40, blank=True)
    iPad_14 = models.CharField(max_length=40, blank=True)
    iPad_15 = models.CharField(max_length=40, blank=True)
    iPad_16 = models.CharField(max_length=40, blank=True)
    pen_01 = models.CharField(max_length=2, blank=True)
    pen_02 = models.CharField(max_length=2, blank=True)
    pen_03 = models.CharField(max_length=2, blank=True)
    pen_04 = models.CharField(max_length=2, blank=True)
    pen_05 = models.CharField(max_length=2, blank=True)
    pen_06 = models.CharField(max_length=2, blank=True)
    pen_07 = models.CharField(max_length=2, blank=True)
    pen_08 = models.CharField(max_length=2, blank=True)
    pen_09 = models.CharField(max_length=2, blank=True)
    pen_10 = models.CharField(max_length=2, blank=True)
    pen_11 = models.CharField(max_length=2, blank=True)
    pen_12 = models.CharField(max_length=2, blank=True)
    pen_13 = models.CharField(max_length=2, blank=True)
    pen_14 = models.CharField(max_length=2, blank=True)
    pen_15 = models.CharField(max_length=2, blank=True)
    pen_16 = models.CharField(max_length=2, blank=True)


class BookingFormIpad(ModelForm):
    class Meta:
        model = Booking
        fields = [
            'iPad_01', 'iPad_02', 'iPad_03', 'iPad_04', 'iPad_05',
            'iPad_06', 'iPad_07', 'iPad_08', 'iPad_09', 'iPad_10',
            'iPad_11', 'iPad_12', 'iPad_13', 'iPad_14', 'iPad_15', 'iPad_16',
            'pen_01', 'pen_02', 'pen_03', 'pen_04', 'pen_05',
            'pen_06', 'pen_07', 'pen_08', 'pen_09', 'pen_10',
            'pen_11', 'pen_12', 'pen_13', 'pen_14', 'pen_15', 'pen_16'
        ]
        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': 'form-control'})


class Room(models.Model):
    short_name = models.CharField(max_length=10)
    room = models.CharField(max_length=50)
    TYPE_CHOICES = [
        ('iPad', 'iPad-Koffer'),
        ('CR', 'Computerraum'),
        ('other', 'anderer Raum'),
    ]
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, blank=True)
    description = models.CharField(max_length=100)
    card = models.IntegerField()
    alert = RichTextField(blank=True)

    def __str__(self):
        return self.short_name
