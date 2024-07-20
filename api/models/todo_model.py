from django.db import models

from api.models.user import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "from " + self.user.username + " - " + self.title

    def save(self, *args, **kwargs):
        super(Todo, self).save(*args, **kwargs)

        return self
