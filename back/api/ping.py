from fastapi import Body, APIRouter

router = APIRouter(tags=["ping"], prefix="")


@router.post('/test')
async def test(payload: dict = Body(...)):
    print(payload)
    return payload
