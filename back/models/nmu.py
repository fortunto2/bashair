from django.db import models
from django_extensions.db.fields import CreationDateTimeField
from django.utils.translation import gettext_lazy as _
from back.models.city import City, Region
from back.models.instance import Instance


class NMU(models.Model):
    """
    Неблагоприятные метереологические условия НМУ. МОгут быть 1, 2, 3. Чем выше тем хуже.
    http://www.meteorb.ru/monitoring/prognoz-zagryazneniya-atmosfery

    Если способствует рассеиванию это отсутствие нму.
    Если способствует  накоплению это  режимы НМУ - незначительное  загрязнение атмосферы  это 1 режим НМУ.
    Повышенное загрязнение атмосферы это 2 режим НМУ. Чрезвычайное 3. На моей памяти 3 не было.

    """

    parse_url = models.URLField()

    MODES = (
        (0, 'Благоприятные'),
        (1, 'НМУ 1'),
        (2, 'НМУ 2'),
        (3, 'НМУ 3'),
    )

    mode = models.IntegerField(
        max_length=9,
        choices=MODES,
        default=0,
    )

    created = CreationDateTimeField(_('created'))
    forecast_date = models.DateTimeField(blank=True, null=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='nmu')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='nmu')

    instance = models.ForeignKey(Instance, on_delete=models.SET_NULL, null=True, related_name='nmu')

