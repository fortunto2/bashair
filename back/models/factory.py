from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class FactoryType(models.Model):
    "Тип, например химическое производство, тэц, мусорка"
    name = models.CharField(max_length=200)


class Factory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    address = models.TextField()
    website = models.URLField(max_length=200)

    location = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)

    factory_type = models.ForeignKey(FactoryType, on_delete=models.SET_NULL, related_name='factory')
    danger_score = models.FloatField(default=0, max_length=1) # условный вред от производства от 1 до 10
