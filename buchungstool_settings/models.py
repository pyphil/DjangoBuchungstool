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
    text =  RichTextField(blank=True)

    def __str__(self):
        return self.setting
