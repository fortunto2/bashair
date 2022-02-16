from pprint import pprint
import sys

from back.time_series.air import InfluxAir

sys.path.append('')


def test_influx_air():
    x = InfluxAir(filters={'city_id': 1})
    assert x
    pprint(x)

    metrics = x.get_metrics()
    assert metrics

    metrics = x.get_history()
    assert metrics
