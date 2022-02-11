from fastapi import APIRouter

from back.models.signal import Signal as SignalModel, SignalToInstance as SignalToInstanceModel, \
    SignalProperties as SignalPropertiesModel
from back.schemas.signal import SignalCreate, SignalToInstanceCreate, Signal, SignalProperties
from back.utils.exceptions import NotFound

router = APIRouter(tags=["signal"], prefix="/signal")


@router.post('/', response_model=Signal)
def create_signal(signal: SignalCreate):
    signal = SignalModel.objects.create(**signal.dict())
    return signal


@router.get('/{signal_id}', response_model=Signal)
def get_signal(signal_id: int):
    try:
        signal = SignalModel.objects.get(id=signal_id)
    except SignalModel.DoesNotExist:
        raise NotFound
    return signal


@router.post('/instance')
def create_signal_to_instance(signal_to_instance: SignalToInstanceCreate):
    signal_to_instance = SignalToInstanceModel.objects.create(**signal_to_instance.dict())
    return signal_to_instance


@router.get('/properties')
def get_properties():
    properties_query = SignalPropertiesModel.objects.all()
    properties = [SignalProperties.from_orm(obj) for obj in properties_query]
    return properties


@router.get('/count')
async def get_count(time=None, city=None, user=None):
    pass
