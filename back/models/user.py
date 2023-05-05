from django.db import models

from back.models.city import City

from django.contrib.auth.models import User
from back.models.community import Community


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cities = models.ManyToManyField(City, related_name='users')
    communities = models.ManyToManyField(Community, blank=True, related_name='members')

