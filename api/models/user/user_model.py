from django.db import models
from .address_model import Address
from .company_model import Company


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    website = models.URLField()
    company = models.OneToOneField(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Users"
        ordering = ['name']
        db_table = 'user'
        managed = True
        abstract = False

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(User, self).delete(*args, **kwargs)


