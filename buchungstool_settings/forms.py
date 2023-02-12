from django.forms import ModelForm
from django import forms
from .models import Setting


class SettingForm(ModelForm):
    class Meta:
        model = Setting
        fields = (
            'school',
            'email_to',
            'noreply_mail',
        )

        widgets = {
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'email_to': forms.TextInput(attrs={'class': 'form-control'}),
            'noreply_mail': forms.TextInput(attrs={'class': 'form-control'}),
        }


class InfoFrontpageForm(ModelForm):
    class Meta:
        model = Setting
        fields = (
            'info_frontpage',
        )
