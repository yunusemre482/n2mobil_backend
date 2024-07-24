from django.db import models
from .post_model import Post


class Comment(models.Model):
    id: models.AutoField(primary_key=True)
    postId = models.ForeignKey(Post, related_name='posts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f"Comment by {self.username} on Post {self.postId}"

    def DOES_NOT_EXIST(self):
        return  Exception("Comment does not exist")