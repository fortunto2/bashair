from django.db import models

from back.models.citys import City
from phonenumber_field.modelfields import PhoneNumberField


class Instance(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    report_url = models.URLField(max_length=200, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='instance')
