"""
Definition of models.

"""

from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    active = models.BooleanField(default=False)
    pendingCallRequest = models.BooleanField(default = False)

class CallRequest(models.Model):
    requestee = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    description = models.TextField()
    time_of_call = models.DateTimeField()
    is_pending = models.BooleanField(default = False)
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(User, related_name = 'completed_requests', on_delete=models.CASCADE, null=True)

