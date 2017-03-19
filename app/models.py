"""
Definition of models.

"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    last_completed_request = models.DateTimeField(default = datetime.datetime.now())
    mmr = models.DecimalField(max_digits=2,decimal_places=1)
    active = models.BooleanField(default=False)
    callFreq = models.DecimalField(default = 1)
    pendingCallRequest = models.BooleanField(default = False)

class Request(models.Model):
    requestee = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    description = models.TextField()
    time_of_call = models.DateTimeField()
    is_pending = models.BooleanField(default = False)
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(User, related_name = 'completed_requests', on_delete=models.CASCADE)

class allowedRequest(models.Model):
    request = models.OneToOneField(Request)
    allowed = models.BooleanField(default = False)

