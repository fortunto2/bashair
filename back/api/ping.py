from fastapi import Body, APIRouter

router = APIRouter()


@router.post('/test')
async def test(payload: dict = Body(...)):
    print(payload)
    return payload
