from django.db import models


class Geo(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return f'{self.lat}, {self.lng}'

    class Meta:
        verbose_name_plural = "Geos"
        ordering = ['lat']
        db_table = 'geo'
        managed = True
        abstract = False

    def save(self, *args, **kwargs):
        super(Geo, self).save(*args, **kwargs)
