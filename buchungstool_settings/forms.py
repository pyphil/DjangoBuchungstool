from django.forms import ModelForm
from django import forms
from .models import Setting
from buchungstool.models import Category


class SettingForm(ModelForm):
    class Meta:
        model = Setting
        fields = (
            'institution',
            'logo',
            'access_token',
            'email_to',
            'noreply_mail',
            'email_host',
            'email_use_tls',
            'email_port',
            'email_host_user',
            'email_host_password',
        )

        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
            # 'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'email_to': forms.TextInput(attrs={'class': 'form-control'}),
            'noreply_mail': forms.TextInput(attrs={'class': 'form-control'}),
            'email_host': forms.TextInput(attrs={'class': 'form-control'}),
            'email_use_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_port': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'email_host_user': forms.TextInput(attrs={'class': 'form-control'}),
            'email_host_password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
        }


class InfoFrontpageForm(ModelForm):
    class Meta:
        model = Setting
        fields = (
            'info_frontpage',
        )


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'color', 'column_break', 'position')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'column_break': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'position': forms.HiddenInput(),
        }
