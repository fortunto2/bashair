from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from back.models.city import City


class Community(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    social = models.URLField(max_length=200, blank=True, null=True)
    social2 = models.URLField(max_length=200, blank=True, null=True)
    social3 = models.URLField(max_length=200, blank=True, null=True)
    news_feed = models.URLField(max_length=200, blank=True, null=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='community')
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='community')
    logo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
