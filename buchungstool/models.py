from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class Booking(models.Model):
    room = models.CharField(max_length=10)
    krzl = models.CharField(max_length=3)
    lerngruppe = models.CharField(max_length=30)
    datum = models.DateField()
    stunde = models.IntegerField()
    iPad_01 = models.CharField(max_length=40, default="|")
    iPad_02 = models.CharField(max_length=40, default="|")
    iPad_03 = models.CharField(max_length=40, default="|")
    iPad_04 = models.CharField(max_length=40, default="|")
    iPad_05 = models.CharField(max_length=40, default="|")
    iPad_06 = models.CharField(max_length=40, default="|")
    iPad_07 = models.CharField(max_length=40, default="|")
    iPad_08 = models.CharField(max_length=40, default="|")
    iPad_09 = models.CharField(max_length=40, default="|")
    iPad_10 = models.CharField(max_length=40, default="|")
    iPad_11 = models.CharField(max_length=40, default="|")
    iPad_12 = models.CharField(max_length=40, default="|")
    iPad_13 = models.CharField(max_length=40, default="|")
    iPad_14 = models.CharField(max_length=40, default="|")
    iPad_15 = models.CharField(max_length=40, default="|")
    iPad_16 = models.CharField(max_length=40, default="|")


class Room(models.Model):
    short_name = models.CharField(max_length=10)
    room = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    card = models.IntegerField()
    alert = HTMLField(blank=True)
