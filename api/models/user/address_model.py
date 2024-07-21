from django.db import models
from .geo_model import Geo


class Address(models.Model):
    street = models.CharField(max_length=100)
    suite = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    geo = models.OneToOneField(Geo, on_delete=models.CASCADE)

    # location = models.PointField() // NOTE : this is a PostGIS specific field to make location based operations easier to perform in the database

    def __str__(self):
        return self.street

