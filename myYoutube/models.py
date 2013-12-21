from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import datetime
from ratings.handlers import RatingHandler, ratings
from ratings.forms import SliderVoteForm


class VideoUrl(models.Model):
    name = models.CharField(max_length=128,unique=True)
    url = models.CharField(max_length=128)
    uploaded = models.DateTimeField()
    score = models.IntegerField(default=0)

    def save(self):
        self.uploaded = datetime.now()
        models.Model.save(self)


class VideoRatingHandler(RatingHandler):

    def post_vote(self, request, vote, created):
        instance = vote.content_object
        score = vote.get_score()
        instance.score = score.average
        # instance.num_votes = score.num_votes
        instance.save()

ratings.register(VideoUrl, VideoRatingHandler)

# ratings.register(VideoUrl, score_range=(1, 10))


