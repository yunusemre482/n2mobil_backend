from django.db import  models


class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']
        db_table = 'company'
        managed = True
        abstract = False