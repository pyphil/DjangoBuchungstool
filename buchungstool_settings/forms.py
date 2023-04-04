from django.forms import ModelForm
from django import forms
from .models import Setting
from buchungstool.models import Category, Room


class SettingForm(ModelForm):
    class Meta:
        model = Setting
        fields = (
            'institution',
            'logo',
            'access_token',
            'student_access_token',
            'email_to',
            'noreply_mail',
            'email_host',
            'email_use_tls',
            'email_port',
            'email_host_user',
            'email_host_password_enc',
        )

        labels = {
            'institution': 'Kurzname der Institution zur Anzeige in der Kopfzeile',
            'logo': 'Hochladen eines Logos',
            'access_token': 'Access Token (Beschränkt den Zugang auf Geräte/Konten der Institution. ' +
                'Das Token sollte möglichst lang sein. Es wird auf folgende Weise als URL-Parameter ' +
                'angehängt, z.B. https://buchungstool.institution.org/?access=2s3x5W6... ' +
                'Diese URL sollte auf berechtigten Konten und Geräten verteilt werden.)',
            'student_access_token': 'Student Access Token für die Nutzerliste. ' +
                'Die URL zur Nutzerliste auf Schülerendgeräten lautet dann z.B. ' +
                'https://buchungstool.institution.org/userlist/select/?access=2s3x5W6... ' +
                'Diese URL sollte auf berechtigten Konten und Geräten zum Eintrag in die Nuterliste verteilt werden.)',
            'email_to': 'Empfänger E-Mail-Adresse für Benachrichtigungen wie Schadenmeldungen',
            'noreply_mail': 'Noreply-Adresse, die als Versandadresse für Benachrichtigungen dient',
            'email_host': 'SMTP-Host für den Versand (z.B.: smtp.office365.com)',
            'email_use_tls': 'TLS-Verschlüsselung nutzen',
            'email_port': 'Port (z.B. 587)',
            'email_host_user': 'Benutzername des noreply-Kontos (i.d.R. identisch mit noreply-Adresse)',
            'email_host_password_enc': 'Passwort des noreply-Kontos (wird verschlüsselt gespeichert)',
        }

        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
            'student_access_token': forms.TextInput(attrs={'class': 'form-control'}),
            # Standard widget for logo instead of form-control 
            # 'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'email_to': forms.TextInput(attrs={'class': 'form-control'}),
            'noreply_mail': forms.TextInput(attrs={'class': 'form-control'}),
            'email_host': forms.TextInput(attrs={'class': 'form-control'}),
            'email_use_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_port': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'email_host_user': forms.TextInput(attrs={'class': 'form-control'}),
            'email_host_password_enc': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
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


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ('room', 'short_name', 'description', 'type', 'category', 
                  'position', 'is_first_of_category', 'is_last_of_category')

        widgets = {
            'room': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select', 'onchange': 'this.form.submit()'}),
            'category': forms.Select(attrs={'class': 'form-select', 'onchange': 'this.form.submit()'}),
            'position': forms.HiddenInput(),
            'is_first_of_category': forms.HiddenInput(),
            'is_last_of_category': forms.HiddenInput(),
        }
