from django.db import models
from ckeditor.fields import RichTextField
from django import forms
from django.forms import ModelForm


class Booking(models.Model):
    room = models.CharField(max_length=10)
    krzl = models.CharField(max_length=3)
    lerngruppe = models.CharField(max_length=30)
    datum = models.DateField()
    stunde = models.IntegerField()
    series_id = models.CharField(max_length=32, blank=True)
    iPad_01 = models.CharField(max_length=40, blank=True)
    iPad_02 = models.CharField(max_length=40, blank=True)
    iPad_03 = models.CharField(max_length=40, blank=True)
    iPad_04 = models.CharField(max_length=40, blank=True)
    iPad_05 = models.CharField(max_length=40, blank=True)
    iPad_06 = models.CharField(max_length=40, blank=True)
    iPad_07 = models.CharField(max_length=40, blank=True)
    iPad_08 = models.CharField(max_length=40, blank=True)
    iPad_09 = models.CharField(max_length=40, blank=True)
    iPad_10 = models.CharField(max_length=40, blank=True)
    iPad_11 = models.CharField(max_length=40, blank=True)
    iPad_12 = models.CharField(max_length=40, blank=True)
    iPad_13 = models.CharField(max_length=40, blank=True)
    iPad_14 = models.CharField(max_length=40, blank=True)
    iPad_15 = models.CharField(max_length=40, blank=True)
    iPad_16 = models.CharField(max_length=40, blank=True)
    iPad_17 = models.CharField(max_length=40, blank=True)
    iPad_18 = models.CharField(max_length=40, blank=True)
    iPad_19 = models.CharField(max_length=40, blank=True)
    iPad_20 = models.CharField(max_length=40, blank=True)
    iPad_21 = models.CharField(max_length=40, blank=True)
    iPad_22 = models.CharField(max_length=40, blank=True)
    iPad_23 = models.CharField(max_length=40, blank=True)
    iPad_24 = models.CharField(max_length=40, blank=True)
    iPad_25 = models.CharField(max_length=40, blank=True)
    iPad_26 = models.CharField(max_length=40, blank=True)
    iPad_27 = models.CharField(max_length=40, blank=True)
    iPad_28 = models.CharField(max_length=40, blank=True)
    iPad_29 = models.CharField(max_length=40, blank=True)
    iPad_30 = models.CharField(max_length=40, blank=True)
    pen_01 = models.CharField(max_length=2, blank=True)
    pen_02 = models.CharField(max_length=2, blank=True)
    pen_03 = models.CharField(max_length=2, blank=True)
    pen_04 = models.CharField(max_length=2, blank=True)
    pen_05 = models.CharField(max_length=2, blank=True)
    pen_06 = models.CharField(max_length=2, blank=True)
    pen_07 = models.CharField(max_length=2, blank=True)
    pen_08 = models.CharField(max_length=2, blank=True)
    pen_09 = models.CharField(max_length=2, blank=True)
    pen_10 = models.CharField(max_length=2, blank=True)
    pen_11 = models.CharField(max_length=2, blank=True)
    pen_12 = models.CharField(max_length=2, blank=True)
    pen_13 = models.CharField(max_length=2, blank=True)
    pen_14 = models.CharField(max_length=2, blank=True)
    pen_15 = models.CharField(max_length=2, blank=True)
    pen_16 = models.CharField(max_length=2, blank=True)
    pen_17 = models.CharField(max_length=2, blank=True)
    pen_18 = models.CharField(max_length=2, blank=True)
    pen_19 = models.CharField(max_length=2, blank=True)
    pen_20 = models.CharField(max_length=2, blank=True)
    pen_21 = models.CharField(max_length=2, blank=True)
    pen_22 = models.CharField(max_length=2, blank=True)
    pen_23 = models.CharField(max_length=2, blank=True)
    pen_24 = models.CharField(max_length=2, blank=True)
    pen_25 = models.CharField(max_length=2, blank=True)
    pen_26 = models.CharField(max_length=2, blank=True)
    pen_27 = models.CharField(max_length=2, blank=True)
    pen_28 = models.CharField(max_length=2, blank=True)
    pen_29 = models.CharField(max_length=2, blank=True)
    pen_30 = models.CharField(max_length=2, blank=True)

class BookingFormIpad(ModelForm):
    class Meta:
        model = Booking
        fields = [
            'iPad_01', 'iPad_02', 'iPad_03', 'iPad_04', 'iPad_05',
            'iPad_06', 'iPad_07', 'iPad_08', 'iPad_09', 'iPad_10',
            'iPad_11', 'iPad_12', 'iPad_13', 'iPad_14', 'iPad_15', 'iPad_16',
            'iPad_12', 'iPad_13', 'iPad_14', 'iPad_15', 'iPad_16', 'iPad_17',
            'iPad_18', 'iPad_19', 'iPad_20', 'iPad_21', 'iPad_22', 'iPad_23',
            'iPad_24', 'iPad_25', 'iPad_26', 'iPad_27', 'iPad_28', 'iPad_29', 'iPad_30',
            'pen_01', 'pen_02', 'pen_03', 'pen_04', 'pen_05',
            'pen_06', 'pen_07', 'pen_08', 'pen_09', 'pen_10',
            'pen_11', 'pen_12', 'pen_13', 'pen_14', 'pen_15', 'pen_16',
            'pen_12', 'pen_13', 'pen_14', 'pen_15', 'pen_16', 'pen_17',
            'pen_18', 'pen_19', 'pen_20', 'pen_21', 'pen_22', 'pen_23',
            'pen_24', 'pen_25', 'pen_26', 'pen_27', 'pen_28', 'pen_29', 'pen_30',
        ]
        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': 'form-control'})


class Category(models.Model):
    def get_next_number():
        """
        Returns the next integer value in the dataset.
        """
        categories = Category.objects.all()
        if categories.count() == 0:
            return 1
        else:
            return categories.aggregate(models.Max('position'))['position__max'] + 1

    name = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField(default=get_next_number)
    color = models.CharField(max_length=7, default='#ebebeb')
    column_break = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['position']


class Room(models.Model):
    def get_next_number():
        """
        Returns the next integer value in the dataset.
        """
        rooms = Room.objects.all()
        if rooms.count() == 0:
            return 1
        else:
            return rooms.aggregate(models.Max('position'))['position__max'] + 1

    short_name = models.CharField(max_length=10)
    room = models.CharField(max_length=50)
    DEVICE_COUNT_CHOICES = []
    for i in range(1,31):
        DEVICE_COUNT_CHOICES.append((str(i), str(i)))
    device_count = models.CharField(max_length=5, choices=DEVICE_COUNT_CHOICES, blank=True)
    description = models.CharField(max_length=100)
    card = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    alert = RichTextField(blank=True)
    position = models.PositiveIntegerField(default=get_next_number)
    is_first_of_category = models.BooleanField(default=False)
    is_last_of_category = models.BooleanField(default=False)

    def __str__(self):
        return f"{ self.room } - { self.description }"

    class Meta:
        ordering = ['category', 'position']


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = RichTextField()

    def __str__(self):
        return self.question
