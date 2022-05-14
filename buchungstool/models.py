from tkinter import Widget
from django.db import models
from tinymce.models import HTMLField
from django import forms
from django.forms import ModelForm

class Booking(models.Model):
    room = models.CharField(max_length=10)
    krzl = models.CharField(max_length=3)
    lerngruppe = models.CharField(max_length=30)
    datum = models.DateField()
    stunde = models.IntegerField()
    iPad_01 = models.CharField(max_length=40, default="|")
    iPad_02 = models.CharField(max_length=40, default="|")
    iPad_03 = models.CharField(max_length=40, default="|")
    iPad_04 = models.CharField(max_length=40, default="|")
    iPad_05 = models.CharField(max_length=40, default="|")
    iPad_06 = models.CharField(max_length=40, default="|")
    iPad_07 = models.CharField(max_length=40, default="|")
    iPad_08 = models.CharField(max_length=40, default="|")
    iPad_09 = models.CharField(max_length=40, default="|")
    iPad_10 = models.CharField(max_length=40, default="|")
    iPad_11 = models.CharField(max_length=40, default="|")
    iPad_12 = models.CharField(max_length=40, default="|")
    iPad_13 = models.CharField(max_length=40, default="|")
    iPad_14 = models.CharField(max_length=40, default="|")
    iPad_15 = models.CharField(max_length=40, default="|")
    iPad_16 = models.CharField(max_length=40, default="|")


class BookingFormIpad(ModelForm):
    class Meta:
        model = Booking
        fields = [
            'iPad_01', 'iPad_02', 'iPad_03', 'iPad_04', 'iPad_05', 
            'iPad_06', 'iPad_07', 'iPad_08', 'iPad_09', 'iPad_10', 
            'iPad_11', 'iPad_12', 'iPad_13', 'iPad_14', 'iPad_15', 'iPad_16'
        ]
        widgets = {
                'iPad_01': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_02': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_03': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_04': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_05': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_06': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_07': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_08': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_09': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_10': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_11': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_12': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_13': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_14': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_15': forms.TextInput(attrs={'class': 'form-control'}),
                'iPad_16': forms.TextInput(attrs={'class': 'form-control'})
        }


class Room(models.Model):
    short_name = models.CharField(max_length=10)
    room = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    card = models.IntegerField()
    alert = HTMLField(blank=True)
