from django.db import models

# Create your models here.


class Booking(models.Model):
    room = models.CharField(max_length=10)
    krzl = models.CharField(max_length=3)
    lerngruppe = models.CharField(max_length=30)
    datum = models.DateField()
    stunde = models.IntegerField()


class Room(models.Model):
    short_name = models.CharField(max_length=10)
    room = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    card = models.IntegerField()
