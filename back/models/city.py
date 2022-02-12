from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from cities_light.abstract_models import (AbstractCity, AbstractRegion, AbstractCountry, AbstractSubRegion)
from cities_light.receivers import connect_default_signals


class Country(AbstractCountry):
    pass


class Region(AbstractRegion):
    pass


class SubRegion(AbstractSubRegion):
    pass


class City(AbstractCity):
    pass


connect_default_signals(City)
