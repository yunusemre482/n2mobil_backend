from django.db import models
from .geo_model import Geo


class Address(models.Model):
    street = models.CharField(max_length=255)
    suite = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=20)
    geo = models.OneToOneField(Geo, on_delete=models.CASCADE)

    def __str__(self):
        return self.street

    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['city']
        db_table = 'address'
        managed = True
        abstract = False

    def save(self, *args, **kwargs):
        super(Address, self).save(*args, **kwargs)

    def get_full_address(self):
        return f'{self.street}, {self.suite}, {self.city}, {self.zipcode}'

