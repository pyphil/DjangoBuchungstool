from django.forms import ModelForm
from django import forms
from .models import Room, FAQ


class RoomAlertForm(ModelForm):
    class Meta:
        model = Room
        fields = (
            'alert',
        )
        labels = {
            'alert': 'Du bist eingeloggt und kannst einen Hinweis zu diesem Raum/Standort erstellen oder bearbeiten'
        }


class FAQForm(ModelForm):
    class Meta:
        model = FAQ
        exclude = {}
        labels = {
            'question': 'Frage',
            'answer': 'Antwort',
        }
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
        }
