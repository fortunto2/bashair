from fastapi import APIRouter

from back.models.signal import Signal, SignalToInstance, SignalProperties
from back.schemas.signal import SignalCreate, SignalToInstanceCreate, SignalGet, SignalProperties, SignalToInstanceGet
from back.utils.exceptions import NotFound

router = APIRouter(tags=["signal"], prefix="/signal")


@router.get('/properties/')
def get_properties():
    properties_query = SignalProperties.objects.all()
    properties = [SignalProperties.from_orm(obj).dict() for obj in properties_query]
    return properties


@router.get('/count/')
async def get_count(time=None, city=None, user=None):
    pass


@router.post('/', response_model=SignalGet)
def create_signal(signal: SignalCreate):
    properties = signal.properties
    signal: Signal = Signal.objects.create(**signal.dict(exclude={'properties'}))
    if properties:
        signal.properties.add(*properties)
    return signal


@router.get('/{signal_id}/', response_model=SignalGet)
def get_signal(signal_id: int):
    try:
        signal = Signal.objects.get(id=signal_id)
    except Signal.DoesNotExist:
        raise NotFound
    return signal


@router.post('/instance/', response_model=SignalToInstanceGet)
def create_signal_to_instance(signal_to_instance: SignalToInstanceCreate):
    signal_to_instance = SignalToInstance.objects.create(**signal_to_instance.dict())
    return signal_to_instance
