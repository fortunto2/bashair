from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from back.models.city import City
from django.contrib.gis.db import models as geomodel

# class FactoryType(models.Model):
#     "Тип, например химическое производство, тэц, мусорка"
#     name = models.CharField(max_length=200)
#     danger_class = models.IntegerField(default=1)


class Factory(TimeStampedModel):
    name = geomodel.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=200,blank=True, null=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='factory')

    # location = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)

    location = geomodel.PointField(blank=True, null=True)

    TYPES = (
        ('zavod', 'Завод'),
        ('musorka', 'Мусорка'),
        ('tec', 'ТЭЦ'),
        ('pred', 'Предприятие'),
        ('other', ''),
    )

    factory_type = models.CharField(
        max_length=9,
        choices=TYPES,
        null=True,
        blank=True
    )

    # factory_type = models.ForeignKey(FactoryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='factory')
    danger_score = models.FloatField(default=0, max_length=1) # условный вред от производства от 1 до 10

    photo = models.ImageField(null=True, blank=True)
    icon = models.FileField(null=True, blank=True)
