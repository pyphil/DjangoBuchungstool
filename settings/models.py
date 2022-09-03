from django.db import models


class Setting(models.Model):
    NAME_CHOICES = [
        ('E-Mail', 'Ziel-E-Mail für Schadenmeldungen'),
        ('noreply-mail', 'noreply-E-Mail zum Versand der Schadenmeldung'),
    ]
    name = models.CharField(max_length=50, choices=NAME_CHOICES)
    setting = models.CharField(max_length=100)

    def __str__(self):
        return self.setting

