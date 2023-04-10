from django.forms import ModelForm
from django import forms
from .models import Setting
from django.utils.safestring import mark_safe
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
            'institution': mark_safe('''
                <div class="mt-3">
                    <strong>Kurzname der Institution zur Anzeige in der Kopfzeile</strong>
                </div>
                '''
            ),
            'logo': mark_safe('''
                <div class="mt-3">
                    <strong>Hochladen eines Logos</strong><br>
                </div>
                '''
            ),
            'access_token': mark_safe('''
                <div class="mt-3">
                    <strong>Access Token</strong><br>
                    <div class="alert alert-info">
                        Das Access-Token beschränkt den Zugang auf Geräte/Konten der Institution.
                        Das Token sollte möglichst lang sein. Es wird auf folgende Weise als URL-Parameter
                        angehängt, z.B. <br>
                        <code>https://buchungstool.institution.org<b><mark>/?access=2s3x5W6...</b></mark></code><br>
                        Diese URL sollte auf berechtigten Konten und Geräten verteilt werden.
                    </div>
                    <div class="alert alert-danger">
                        Nach dem Speichern ist die Seite nur noch über den Link mit Access Token erreichbar. 
                        Das Token kann aber auch über das Django Admin-Backend geändert werden.
                    </div>
                    Aktuelles Token für den Zugriff auf Buchungen und Support Tickets:
                </div>
                '''
            ),
            'student_access_token': mark_safe('''
                <div class="mt-3">
                    <strong>Student Access Token für die Nutzerliste</strong>
                    <div class="alert alert-info">
                        Die URL zur Nutzerliste auf Schülerendgeräten lautet dann z.B.<br>
                        <code>https://buchungstool.institution.org<b><mark>/userlist/select/?access=2s3x5W6...</b></mark></code><br>
                        Diese URL sollte auf berechtigten Konten und Geräten zum Eintrag in die Nutzerliste verteilt werden.
                    </div>
                    Aktuelles Token für den Zugriff auf die Nutzerliste:
                </div>
                '''
            ),
            'email_to': mark_safe('''
                <div class="mt-3">
                    <h3>E-Mail-Konfiguration</h3>
                     <div class="alert alert-info">
                        Um Benachrichtigungen über neue oder im Status geänderte Support Tickets (Schaden- und Problemmitteilungen)
                        zu erhalten, kann hier die SMPT-E-Mail-Konfiguration vorgenommen werden.
                     </div>
                    <strong>Empfänger E-Mail-Adresse für Benachrichtigungen wie Schadenmeldungen</strong>
                '''
            ),
            'noreply_mail': mark_safe('''
                <div class="mt-3">
                    <strong>Noreply-Adresse, die als Versandadresse für Benachrichtigungen dient</strong>
                '''
            ),
            'email_host': mark_safe('''
                <div class="mt-3">
                    <strong>SMTP-Host für den Versand (z.B.: smtp.office365.com)</strong>
                '''
            ),
            'email_use_tls': mark_safe('''
                <div class="mt-3">
                    <strong>TLS-Verschlüsselung nutzen</strong>
                '''
            ),
            'email_port': mark_safe('''
                <div class="mt-3">
                    <strong>Port (bei TLS z.B. standardmäßig 587)</strong>
                '''
            ),
            'email_host_user': mark_safe('''
                <div class="mt-3">
                    <strong>Benutzername des noreply-Kontos (i.d.R. identisch mit noreply-Adresse)</strong>
                '''
            ),
            'email_host_password_enc': mark_safe('''
                <div class="mt-3">
                    <strong>Passwort des noreply-Kontos (wird verschlüsselt gespeichert)</strong>
                '''
            ),
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
