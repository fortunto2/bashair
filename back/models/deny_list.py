from django.db import models


class DenyList(models.Model):
    jti = models.TextField()
