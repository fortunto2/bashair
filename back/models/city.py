from cities_light.abstract_models import (AbstractCity, AbstractRegion, AbstractCountry, AbstractSubRegion)
from cities_light.receivers import connect_default_signals
from django.contrib.gis.db import models as geomodel
from django.contrib.gis.geos import Point


class Country(AbstractCountry):
    pass


class Region(AbstractRegion):
    pass


class SubRegion(AbstractSubRegion):
    pass


class City(AbstractCity):
    point = geomodel.PointField(null=True)

    def save(self, *args, **kwargs):

        if not self.point:
            self.point = Point(self.longitude, self.latitude)

        self.latitude = self.point.y
        self.longitude = self.point.x
        super().save(*args, **kwargs)


connect_default_signals(City)
