from fastapi import APIRouter

from back.schemas.signal import SignalCreate, SignalToInstanceCreate

router = APIRouter(tags=["signal"], prefix="/signal")


@router.post('/')
async def create_signal(signal: SignalCreate):
    pass


@router.get('/{signal_id}')
async def get_signal(signal_id: int):
    pass


@router.post('/instance')
async def create_signal_to_instance(signa_to_instance: SignalToInstanceCreate):
    pass


@router.get('/properties')
async def get_properties():
    pass


@router.get('/count')
async def get_count(time=None, city=None, user=None):
    pass
