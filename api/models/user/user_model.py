from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .address_model import Address
from .company_model import Company
from uuid import uuid4
from django.contrib.auth.models import UserManager

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    website = models.URLField()
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['id', 'email']

    objects = UserManager()

    def __str__(self):
        return self.username



    class Meta:
        verbose_name_plural = "Users"
        ordering = ['name']
        db_table = 'user'
        managed = True
        abstract = False
