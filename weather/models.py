from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class City(models.Model):
    city = models.CharField(max_length=25)
    date = models.DateTimeField(default=timezone.now)


class Pref(models.Model):
    max_wind = models.IntegerField()
    min_temp = models.IntegerField()
