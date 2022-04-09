from django.db import models

# Create your models here.


class Booking(models.Model):
    room = models.CharField(max_length=10)
    krzl = models.CharField(max_length=3)
    lerngruppe = models.CharField(max_length=30)
    datum = models.DateField()
    stunde = models.IntegerField()
    iPad_01 = models.CharField(max_length=40, default="0|0")
    iPad_02 = models.CharField(max_length=40, default="0|0")
    iPad_03 = models.CharField(max_length=40, default="0|0")
    iPad_04 = models.CharField(max_length=40, default="0|0")
    iPad_05 = models.CharField(max_length=40, default="0|0")
    iPad_06 = models.CharField(max_length=40, default="0|0")
    iPad_07 = models.CharField(max_length=40, default="0|0")
    iPad_08 = models.CharField(max_length=40, default="0|0")
    iPad_09 = models.CharField(max_length=40, default="0|0")
    iPad_10 = models.CharField(max_length=40, default="0|0")
    iPad_11 = models.CharField(max_length=40, default="0|0")
    iPad_12 = models.CharField(max_length=40, default="0|0")
    iPad_13 = models.CharField(max_length=40, default="0|0")
    iPad_14 = models.CharField(max_length=40, default="0|0")
    iPad_15 = models.CharField(max_length=40, default="0|0")
    iPad_16 = models.CharField(max_length=40, default="0|0")


class Room(models.Model):
    short_name = models.CharField(max_length=10)
    room = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    card = models.IntegerField()
