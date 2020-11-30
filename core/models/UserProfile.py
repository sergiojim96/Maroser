from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.CharField(max_length=40)
    email = models.CharField(max_length=40, blank=True, null=True)
    provincia = models.CharField(max_length=40, blank=True, null=True)
    canton = models.CharField(max_length=40, blank=True, null=True)
    address = models.CharField(max_length=40, blank=True, null=True)
    distrito = models.CharField(max_length=40, blank=True, null=True)


    def __str__(self):
        return self.user
