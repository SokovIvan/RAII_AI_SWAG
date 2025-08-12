from django.db import models

from tickets import Ticket

class AudioManager(models.Model):
    def create(self, record):
        audio = self.model(record = record)
        
        audio.save()

class Audio(models.Model):
    record = models.FileField(upload_to=None)
    text = models.CharField()
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL)
    objects  = AudioManager()