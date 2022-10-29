from django.db import models
from tinymce.models import HTMLField
from django import forms
from django.forms import ModelForm


# iPads = [
#     {'dbname': 'iPad_01', 'name': 'iPad 01'},
#     {'dbname': 'iPad_02', 'name': 'iPad 02'},
#     {'dbname': 'iPad_03', 'name': 'iPad 03'},
#     {'dbname': 'iPad_04', 'name': 'iPad 04'},
#     {'dbname': 'iPad_05', 'name': 'iPad 05'},
#     {'dbname': 'iPad_06', 'name': 'iPad 06'},
#     {'dbname': 'iPad_07', 'name': 'iPad 07'},
#     {'dbname': 'iPad_08', 'name': 'iPad 08'},
#     {'dbname': 'iPad_09', 'name': 'iPad 09'},
#     {'dbname': 'iPad_10', 'name': 'iPad 10'},
#     {'dbname': 'iPad_11', 'name': 'iPad 11'},
#     {'dbname': 'iPad_12', 'name': 'iPad 12'},
#     {'dbname': 'iPad_13', 'name': 'iPad 13'},
#     {'dbname': 'iPad_14', 'name': 'iPad 14'},
#     {'dbname': 'iPad_15', 'name': 'iPad 15'},
#     {'dbname': 'iPad_16', 'name': 'iPad 16'},
# ]

# pens = [
#     {'dbname': 'pen_01', 'name': 'pen 01', },
#     {'dbname': 'pen_02', 'name': 'pen 02', },
#     {'dbname': 'pen_03', 'name': 'pen 03', },
#     {'dbname': 'pen_04', 'name': 'pen 04', },
#     {'dbname': 'pen_05', 'name': 'pen 05', },
#     {'dbname': 'pen_06', 'name': 'pen 06', },
#     {'dbname': 'pen_07', 'name': 'pen 07', },
#     {'dbname': 'pen_08', 'name': 'pen 08', },
#     {'dbname': 'pen_09', 'name': 'pen 09', },
#     {'dbname': 'pen_10', 'name': 'pen 10', },
#     {'dbname': 'pen_11', 'name': 'pen 11', },
#     {'dbname': 'pen_12', 'name': 'pen 12', },
#     {'dbname': 'pen_13', 'name': 'pen 13', },
#     {'dbname': 'pen_14', 'name': 'pen 14', },
#     {'dbname': 'pen_15', 'name': 'pen 15', },
#     {'dbname': 'pen_16', 'name': 'pen 16', },
# ]


class Booking(models.Model):
    room = models.CharField(max_length=10)
    krzl = models.CharField(max_length=3)
    lerngruppe = models.CharField(max_length=30)
    datum = models.DateField()
    stunde = models.IntegerField()
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


class BookingFormIpad(ModelForm):
    class Meta:
        model = Booking
        fields = [
            'iPad_01', 'iPad_02', 'iPad_03', 'iPad_04', 'iPad_05',
            'iPad_06', 'iPad_07', 'iPad_08', 'iPad_09', 'iPad_10',
            'iPad_11', 'iPad_12', 'iPad_13', 'iPad_14', 'iPad_15', 'iPad_16',
            'pen_01', 'pen_02', 'pen_03', 'pen_04', 'pen_05',
            'pen_06', 'pen_07', 'pen_08', 'pen_09', 'pen_10',
            'pen_11', 'pen_12', 'pen_13', 'pen_14', 'pen_15', 'pen_16'
        ]
        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': 'form-control'})
        # widgets = {
        #         'iPad_01': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_02': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_03': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_04': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_05': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_06': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_07': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_08': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_09': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_10': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_11': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_12': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_13': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_14': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_15': forms.TextInput(attrs={'class': 'form-control'}),
        #         'iPad_16': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_01': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_02': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_03': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_04': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_05': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_06': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_07': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_08': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_09': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_10': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_11': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_12': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_13': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_14': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_15': forms.TextInput(attrs={'class': 'form-control'}),
        #         'pen_16': forms.TextInput(attrs={'class': 'form-control'})
        # }


class Room(models.Model):
    short_name = models.CharField(max_length=10)
    room = models.CharField(max_length=50)
    TYPE_CHOICES = [
        ('iPad', 'iPad-Koffer'),
        ('CR', 'Computerraum'),
        ('other', 'anderer Raum'),
    ]
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, blank=True)
    description = models.CharField(max_length=100)
    card = models.IntegerField()
    alert = HTMLField(blank=True)

    def __str__(self):
        return self.short_name
