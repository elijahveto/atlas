from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name= models.CharField(max_length = 100, blank=False, null=False)
    membership = models.CharField(default='free', max_length=10)
    reg_date = models.DateField(default=datetime.now)
    has_manager = models.BooleanField(default=False)


class User(AbstractUser):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)