# https://github.com/opendata-stuttgart/feinstaub-api/blob/master/feinstaub/sensors/models.py

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel

from back.api.weather import get_weather
from back.models.base import LocationModel
from back.models.city import City

from back.time_series.air import InfluxAir


class SensorType(TimeStampedModel):
    uid = models.SlugField(unique=True)
    name = models.CharField(max_length=1000)
    manufacturer = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000, null=True, blank=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.uid


class Node(TimeStampedModel, LocationModel):  # ЭТО ДАТЧИК!
    uid = models.SlugField(unique=True)
    mac = models.CharField(null=True, blank=True, max_length=20)
    name = models.CharField(null=True, blank=True, max_length=200, validators=[MinLengthValidator(7)])
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='node')

    height = models.IntegerField(null=True)

    description = models.TextField(null=True, blank=True)

    # propertys
    sensor_position = models.IntegerField(null=True, blank=True)  # 0 = no information, 1 = in backyard, 10 = just in front of the house at the street
    traffic_in_area = models.IntegerField(null=True, blank=True)  # 0 = no information, 1 = far away from traffic, 10 = lot's of traffic in area
    oven_in_area = models.IntegerField(null=True, blank=True)  # 0 = no information, 1 = no ovens in area, 10 = it REALLY smells
    industry_in_area = models.IntegerField(null=True, blank=True)  # 0 = no information, 1 = no industry in area, 10 = industry all around

    indoor = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)

    class Meta:
        ordering = ['uid', ]

    def __str__(self):
        return self.uid

    def get_metrics(self):

        influx = InfluxAir(filters={'node': self.uid})
        metrics = influx.get_metrics()

        return metrics

    def get_history(self):
        influx = InfluxAir(filters={'node': self.uid})
        history = influx.get_history()

        return history

    @property
    def wind(self):
        return get_weather(latitude=self.latitude, longitude=self.longitude)

    # @property
    # def city(self):
    #     return self.city.name


SENSOR_TYPE_CHOICES = (
    # ppd42ns P1 -> 1µm / SDS011 P1 -> 10µm
    ('P0', '1µm particles'),
    ('P1', '10µm particles'),
    ('P2', '2.5µm particles'),
    ('durP1', 'duration 1µm'),
    ('durP2', 'duration 2.5µm'),
    ('ratioP1', 'ratio 1µm in percent'),
    ('ratioP2', 'ratio 2.5µm in percent'),
    ('samples', 'samples'),
    ('min_micro', 'min_micro'),
    ('max_micro', 'max_micro'),
    # sht10-sht15; dht11, dht22; bmp180, bme280
    ('temperature', 'Temperature'),
    # sht10-sht15; dht11, dht22, bme280
    ('humidity', 'Humidity'),
    # bmp180, bme280
    ('pressure', 'Pa'),
    ('altitude', 'meter'),
    ('pressure_sealevel', 'Pa (sealevel)'),
    #
    ('brightness', 'Brightness'),
    # gp2y10
    ('dust_density', 'Dust density in mg/m3'),
    ("vo_raw", 'Dust voltage raw'),
    ("voltage", "Dust voltage calculated"),
    # dsm501a
    ('P10', '1µm particles'),  # identical to P1
    ('P25', '2.5µm particles'),  # identical to P2
    ('durP10', 'duration 1µm'),
    ('durP25', 'duration 2.5µm'),
    ('ratioP10', 'ratio 1µm in percent'),
    ('ratioP25', 'ratio 2.5µm in percent'),
    ##
    ('door_state', 'door state (open/closed)'),
    ## gpssensor
    ('lat', 'latitude'),
    ('lon', 'longitude'),
    ('height', 'height'),
    ('hdop', 'horizontal dilusion of precision'),
    ('timestamp', 'measured timestamp'),
    ('age', 'measured age'),
    ('satelites', 'number of satelites'),
    ('speed', 'current speed over ground'),
    ('azimuth', 'track angle'),
    ## noise sensor
    ('noise_L01', 'Sound level L01'),
    ('noise_L95', 'Sound level L95'),
    ('noise_Leq', 'Sound level Leq'),
    ##gas sensor
    ('co_kohm', 'CO in kOhm'),
    ('co_ppb', 'CO in ppb'),
    ('eco2', 'eCO2 in ppm'),
    ('no2_kohm', 'NO2 in kOhm'),
    ('no2_ppb', 'NO2 in ppb'),
    ('ozone_ppb', 'O3 in ppb'),
    ('so2_ppb', 'SO2 in ppb'),
)

