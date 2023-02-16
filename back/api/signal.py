from datetime import datetime, timedelta
from typing import List

from django.contrib.auth.models import User
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi_cache.decorator import cache

from back.depends.user import get_current_active_user
from back.models.signal import Signal, SignalToInstance, SignalProperties
from back.models.signal import SignalProperties as SignalPropertiesModel
from back.schemas.signal import SignalCreate, SignalToInstanceCreate, SignalGet, SignalProperties, SignalToInstanceGet
from back.utils.exceptions import NotFound

router = APIRouter(tags=["signal"], prefix="/signal")


@router.get('/properties')
@cache(expire=360)
def get_properties():
    """
    Для формы жалобы, параметры такие как возможные запахи и симптомы
    """
    properties_query = SignalPropertiesModel.objects.all()
    properties = [SignalProperties.from_orm(obj).dict() for obj in properties_query]
    return properties


@router.get('/count')
def get_count(time=None, city=None, user=None):
    """
    Количество жалоб счетчик
    """
    # todo: фильтровать через инфлюкс по параметрам
    count_query = Signal.objects.count()
    return int(count_query)


@router.post('/send', response_model=SignalGet)
def create_signal(signal: SignalCreate, user: User = Depends(get_current_active_user)):
    """
    Create a signal record in the database
    """
    properties = signal.properties
    signal_dict = signal.dict(exclude={"properties"})
    signal = Signal(**signal_dict)
    signal.owner = user
    signal.owner_id = user.id
    signal.save()
    if properties:
        try:
            signal.properties.add(*properties)
        except Exception as e:
            signal.delete()
            raise HTTPException(status_code=400, detail=str(e))
    return signal

@router.get('/{signal_id}', response_model=SignalGet)
def get_signal(signal_id: int):
    """
    Данные по конкретной жалобе подробнее
    """
    try:
        signal = Signal.objects.get(id=signal_id)
    except Signal.DoesNotExist:
        raise NotFound
    return signal


@router.get("/all/", response_model=List[SignalGet])
def get_signals():
    """Get all Signal instances created within the last 24 hours"""
    time_threshold = datetime.now() - timedelta(hours=24)
    # signals = Signal.objects.filter(created__gte=time_threshold, city_id=1)
    # get signals use sync_to_async
    signals = Signal.objects.filter(created__gte=time_threshold, city_id=1)

    return list(signals)


@router.post('/instance', response_model=SignalToInstanceGet)
def create_signal_to_instance(signal_to_instance: SignalToInstanceCreate, user: User = Depends(get_current_active_user)):
    """
    Для формы жалобы в инстанции различные, такие как ЕДДС
    """
    signal_to_instance = SignalToInstance.objects.create(**signal_to_instance.dict())
    return signal_to_instance
