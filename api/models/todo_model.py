from datetime import datetime

from django.db import models

from api.models.user import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now,null=True, blank=True)
    updated_at = models.DateTimeField(default=datetime.now,null=True, blank=True)
    def __str__(self):
        return "from " + self.user.username + " - " + self.title

    def save(self, *args, **kwargs):
        super(Todo, self).save(*args, **kwargs)

        return self
