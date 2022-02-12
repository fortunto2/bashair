from django.db import models


class Token(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_type = models.TextField()
    ttl = models.BigIntegerField()
