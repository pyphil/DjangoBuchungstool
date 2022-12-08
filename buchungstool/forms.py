from django.forms import ModelForm
from django import forms
from .models import Room


class RoomAlertForm(ModelForm):
    class Meta:
        model = Room
        fields = (
            'alert',
        )
        labels = {
            'alert': 'Du bist eingeloggt und kannst einen Hinweis zu diesem Raum/Gerät erstellen oder bearbeiten'
        }
