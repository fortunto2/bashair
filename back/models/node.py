# https://github.com/opendata-stuttgart/feinstaub-api/blob/master/feinstaub/sensors/models.py

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.timezone import now

from back.models.city import City
from config.influx import query_api
from config.owm import weather_manager


class SensorType(TimeStampedModel):
    uid = models.SlugField(unique=True)
    name = models.CharField(max_length=1000)
    manufacturer = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000, null=True, blank=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.uid


class Node(TimeStampedModel):  # ЭТО ДАТЧИК!
    uid = models.SlugField(unique=True)
    # mac = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    height = models.IntegerField(null=True)
    sensor_position = models.IntegerField(
        null=True)  # 0 = no information, 1 = in backyard, 10 = just in front of the house at the street
    location = models.ForeignKey("SensorLocation", on_delete=models.DO_NOTHING)
    # email = models.EmailField(null=True, blank=True)
    last_notify = models.DateTimeField(null=True, blank=True)
    description_internal = models.TextField(null=True,
                                            blank=True)  # for internal purposes, should never been provided via API / dump / ...
    indoor = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    exact_location = models.BooleanField(default=False)

    class Meta:
        ordering = ['uid', ]

    def __str__(self):
        return self.uid

    @property
    def pm25(self):
        result = query_api.query_csv(f"""
        from(bucket: "air")
          |> range(start: -15m)
          |> filter(fn: (r) => r["node"] == "{self.uid}")
          |> filter(fn: (r) => r["_field"] == "pm25")
          |> aggregateWindow(every: 15m, fn: mean, createEmpty: false)
          |> last()
        """)
        value = None
        value_index = None
        for row in result:
            if len(row) > 1:
                if row[1] == 'result' and value_index is None:
                    value_index = next((index for index, col in enumerate(row) if col == '_value'), None)
                if row[0] == '' and row[1] == '' and value_index is not None:
                    value = row[value_index]
        return value

    @property
    def wind(self):
        if self.location.latitude is not None and self.location.longitude is not None:
            try:
                response = weather_manager.weather_at_coords(
                    lat=float(self.location.latitude),
                    lon=float(self.location.longitude)
                )
                return response.weather.wnd
            except Exception as e:
                print(f'WARNING! Error weather API: {e}')
        return {}


class Sensor(TimeStampedModel):  # ЭТО СЕНСОР!
    node = models.ForeignKey(Node, related_name="sensors", on_delete=models.DO_NOTHING)
    pin = models.CharField(
        max_length=10,
        default='-',
        db_index=True,
        help_text='differentiate the sensors on one node by giving pin used',
    )
    sensor_type = models.ForeignKey(SensorType, on_delete=models.DO_NOTHING)
    description = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=True, db_index=True)

    class Meta:
        unique_together = ('node', 'pin')

    def __str__(self):
        return "{} {}".format(self.node, self.pin)


# class SensorData(TimeStampedModel):
#     sensor = models.ForeignKey(Sensor, related_name="sensordatas", on_delete=models.DO_NOTHING)
#     sampling_rate = models.IntegerField(null=True, blank=True,
#                                         help_text="in milliseconds")
#     timestamp = models.DateTimeField(default=now, db_index=True)
#     location = models.ForeignKey("SensorLocation", blank=True, on_delete=models.DO_NOTHING)
#     software_version = models.CharField(max_length=100, default="",
#                                         help_text="sensor software version")
#
#     class Meta(TimeStampedModel.Meta):
#         index_together = (('modified',),)
#
#     def __str__(self):
#         return "{sensor} [{value_count}]".format(
#             sensor=self.sensor, value_count=self.sensordatavalues.count())


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


# class SensorDataValue(TimeStampedModel):
#     sensordata = models.ForeignKey(SensorData, related_name='sensordatavalues', on_delete=models.DO_NOTHING)
#     value = models.TextField(null=False)
#     value_type = models.CharField(max_length=100, choices=SENSOR_TYPE_CHOICES,
#                                   db_index=True)
#
#     class Meta:
#         unique_together = (('sensordata', 'value_type',),)
#
#     def __str__(self):
#         return "{sensordata}: {value} [{value_type}]".format(
#             sensordata=self.sensordata,
#             value=self.value,
#             value_type=self.value_type,
#         )


class SensorLocation(TimeStampedModel):
    location = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)
    altitude = models.DecimalField(max_digits=14, decimal_places=8, null=True, blank=True)
    indoor = models.BooleanField(default=False)
    street_name = models.TextField(null=True, blank=True)
    street_number = models.TextField(null=True, blank=True)
    postalcode = models.TextField(null=True, blank=True)
    # city_old = models.TextField(null=True, blank=True)
    # country = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='sensor_location')
    traffic_in_area = models.IntegerField(
        null=True)  # 0 = no information, 1 = far away from traffic, 10 = lot's of traffic in area
    oven_in_area = models.IntegerField(null=True)  # 0 = no information, 1 = no ovens in area, 10 = it REALLY smells
    industry_in_area = models.IntegerField(
        null=True)  # 0 = no information, 1 = no industry in area, 10 = industry all around
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING,
                              help_text="If not set, location is public.")
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['location', ]
        # indexes = [
        #     # models.Index(fields=['country'], name='country_idx'),
        #     # models.Index(fields=['city'], name='city_idx'),
        # ]

    def __str__(self):
        return "{location}".format(location=self.location)
