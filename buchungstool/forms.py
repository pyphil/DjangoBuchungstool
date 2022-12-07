from django.forms import ModelForm
from django import forms
from .models import Room


class RoomAlertForm(ModelForm):
    class Meta:
        model = Room
        fields = (
            'alert',
        )
        # alert = forms.CharField()
