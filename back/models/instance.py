from django.db import models

from back.models.citys import City


class Instance(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    address = models.TextField()
    website = models.URLField(max_length=200)
    report_url = models.URLField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='instance')

