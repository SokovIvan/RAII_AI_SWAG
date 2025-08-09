from django.db import models

from processing.models import Audio

class Ticket(models.Model):
    audio = models.ForeignKey(Audio, on_delete=models.SET_NULL)