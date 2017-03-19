"""
Definition of models.

"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    active = models.BooleanField(default=False)

class Request(models.Model):
    requestee = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    description = models.TextField()
    time_of_call = models.DateTimeField(required=True)
    is_taken = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
