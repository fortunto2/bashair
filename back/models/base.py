from django.contrib.gis.db import models as geomodel
from django.db import models

from back.models.city import City


class LocationModel(models.Model):
    """
    Location

    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    point = geomodel.PointField(null=True)

    # заполняется автоматом на основе координат
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)

    street_name = models.CharField(null=True, blank=True, max_length=200)
    street_number = models.CharField(null=True, blank=True, max_length=10)
    postalcode = models.CharField(null=True, blank=True, max_length=6)

    def save(self):
        self.latitude = self.point.y
        self.longitude = self.point.x
        super(LocationModel, self).save()

    class Meta:
        abstract = True
