from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from back.models.instance import Instance


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


class Signal(TimeStampedModel):
    text = models.TextField()
    properties = models.ManyToManyField(SignalProperties, related_name='reports')
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reports')
    location = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)

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
