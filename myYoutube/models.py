from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import datetime

class VideoUrl(models.Model):
    name = models.CharField(max_length=128,unique=True)
    url = models.CharField(max_length=128)
    uploaded = models.DateTimeField()
    # rate_choices=(
    #     ('5',5),
    #     ('4',4),
    #     )
    # score=models.IntegerField(default=0,choices=rate_choices)
    def save(self):
        self.uploaded = datetime.now()
        models.Model.save(self)