from django.contrib.auth.models import User
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from back.depends.user import get_current_active_user
from back.models.signal import Signal, SignalToInstance, SignalProperties
from back.models.signal import SignalProperties as SignalPropertiesModel
from back.schemas.signal import SignalCreate, SignalToInstanceCreate, SignalGet, SignalProperties, SignalToInstanceGet
from back.utils.exceptions import NotFound

router = APIRouter(tags=["signal"], prefix="/signal")


@router.get('/properties/')
def get_properties():
    """
    Для формы жалобы, параметры такие как возможные запахи и симптомы
    """
    properties_query = SignalPropertiesModel.objects.all()
    properties = [SignalProperties.from_orm(obj).dict() for obj in properties_query]
    return properties


@router.get('/count/')
async def get_count(time=None, city=None, user=None):
    """
    Количество жалоб счетчик
    """
    return 69


@router.post(
    '/',
    response_model=SignalGet
)
def create_signal(signal: SignalCreate, user: User = Depends(get_current_active_user)):
    """
    Создаем запись с жалобой в базу
    """
    properties = signal.properties
    signal: Signal = Signal.objects.create(owner_id=user.id, **signal.dict(exclude={'properties'}))
    if properties:
        signal.properties.add(*properties)
    return signal


@router.get('/{signal_id}/', response_model=SignalGet)
def get_signal(signal_id: int):
    """
    Данные по конкретной жалобе подробнее
    """
    try:
        signal = Signal.objects.get(id=signal_id)
    except Signal.DoesNotExist:
        raise NotFound
    return signal


@router.post('/instance/', response_model=SignalToInstanceGet)
def create_signal_to_instance(signal_to_instance: SignalToInstanceCreate, user: User = Depends(get_current_active_user)):
    """
    Для формы жалобы в инстанции различные, такие как ЕДДС
    """
    signal_to_instance = SignalToInstance.objects.create(**signal_to_instance.dict())
    return signal_to_instance
