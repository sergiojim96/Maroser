from django.contrib.sessions.models import Session
from django.conf import settings
from django.db import models

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.CharField(max_length=40)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
