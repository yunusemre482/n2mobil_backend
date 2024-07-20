from django.db import models
from . import user


class Album(models.Model):
    userId = models.ForeignKey(user.User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Albums"
        ordering = ['title']
        db_table = 'album'
        managed = True
        abstract = False
