from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from back.models.base import LocationModel
from back.models.instance import Instance

from back.models.city import City


class SignalProperties(models.Model):
    """
    Симптомы и свойства, например газа на вкус.
    Человек отмечает в чекбоксе, что голова болит и тп.
    """
    name = models.TextField()

    GROUPS = (
        ('smells', 'Запахи'),
        ('symptoms', 'Симптомы'),
    )
    group = models.CharField(
        max_length=9,
        choices=GROUPS,
        default='smells',
    )

    def __str__(self):
        return f"{self.name} ({self.group})"


class Signal(TimeStampedModel, LocationModel):
    text = models.TextField()
    properties = models.ManyToManyField(SignalProperties, related_name='reports')
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reports')

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='signal')

    time_of_incident = models.DateTimeField(auto_now=True)

    SIGNAL_STATUS = (
        ('sent', 'Отправлено'),
        ('verified', 'Подтверждено'),
        ('canceled', 'Отмена'),
    )
    status = models.CharField(
        max_length=15,
        choices=SIGNAL_STATUS,
        default='sent',
    )

    def __str__(self):
        return f"{self.text} ({self.time_of_incident.strftime('%Y-%m-%d %H:%M:%S')})"


class SignalMedia(TimeStampedModel):
    signal = models.ForeignKey(Signal, null=True, on_delete=models.SET_NULL, related_name='media')
    file = models.FileField(upload_to='')  # TODO: добавить в env


class SignalToInstance(TimeStampedModel):
    text = models.TextField()
    signal = models.ForeignKey(Signal, null=True, on_delete=models.SET_NULL)
    instance = models.ForeignKey(Instance, null=True, on_delete=models.SET_NULL)
    time_of_report = models.DateTimeField(auto_now=True)

    response = models.TextField()
    time_of_response = models.DateTimeField(auto_now=True)

    STATUSES = (
        ('in_processing', 'В обработке'),
        ('ignore', 'Не дали ответ'),
        ('answered', 'Ответили'),
        ('failed_to_call', 'Не удалось дозвониться'),
        ('other', 'Другое'),
    )
    status = models.CharField(
        max_length=15,
        choices=STATUSES,
        default='in_processing',
    )
    other_comment = models.TextField()


class SignalToInstanceMedia(TimeStampedModel):
    signal = models.ForeignKey(SignalToInstance, null=True, on_delete=models.SET_NULL, related_name='media')
    file = models.FileField(upload_to='')  # TODO: добавить в env
