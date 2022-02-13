from typing import Optional

from fastapi import APIRouter

from back.models.community import Community as CommunityModel
from back.models.factory import Factory
from back.schemas.community import Community
from back.schemas.factory import FactoryGet, ListFactories
from back.utils.exceptions import NotFound

router = APIRouter(tags=["factory"], prefix="/factory")


@router.get('/all', response_model=ListFactories)
def get_factories(city_id: Optional[int] = None):
    """
    Список всех возможных источников загрязнения
    """

    try:
        if city_id:
            factories = Factory.objects.filter(city_id=city_id)
        else:
            factories = Factory.objects.all()
    except Factory.DoesNotExist:
        raise NotFound

    return list(factories)


@router.get('/{factory_id}', response_model=FactoryGet)
def get_factory(factory_id: int):
    """
     Завод по айди
    """

    try:
        factories = Factory.objects.get(id=factory_id)
    except Factory.DoesNotExist:
        raise NotFound

    return factories
