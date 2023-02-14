from django.db import models
# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField


class Config(models.Model):
    NAME_CHOICES = [
        ('E-Mail', 'Ziel-E-Mail für Schadenmeldungen'),
        ('noreply-mail', 'noreply-E-Mail zum Versand der Schadenmeldung'),
        ('info-frontpage', 'info-frontpage'),
    ]
    name = models.CharField(max_length=50, choices=NAME_CHOICES)
    setting = models.CharField(max_length=30, blank=True)
    text = RichTextField(blank=True)

    def __str__(self):
        return self.setting


class Setting(models.Model):
    name = models.CharField(max_length=50, blank=True)
    school = models.CharField(max_length=50, blank=True)
    access_token = models.CharField(max_length=200, blank=True)
    email_to = models.CharField(max_length=50, blank=True)
    noreply_mail = models.CharField(max_length=50, blank=True)
    email_host = models.CharField(max_length=50, blank=True)
    email_use_tls = models.BooleanField(default=True)
    email_port = models.IntegerField(default=587)
    email_host_user = models.CharField(max_length=50, blank=True)
    email_host_password = models.CharField(max_length=50, blank=True)
    info_frontpage = RichTextField(blank=True)
