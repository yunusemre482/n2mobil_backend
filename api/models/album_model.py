from django.db import models
from api.models.user import User


class Album(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Album, self).save(*args, **kwargs)

        return self
