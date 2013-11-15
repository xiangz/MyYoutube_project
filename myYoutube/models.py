from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import datetime

class VideoUrl(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    uploaded = models.DateTimeField()
    def save(self):
        self.uploaded = datetime.now()
        models.Model.save(self)