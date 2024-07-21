from django.db import models


class Geo(models.Model):
    lat = models.CharField(max_length=20) # NOTE : lat double precision NOT NULL,
    lng = models.CharField(max_length=20) # NOTE   lng double precision NOT NULL, correct version of this code is below


