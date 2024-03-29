from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@router.get("/ping", status_code=200)
async def pong() -> dict:
    return {"ping": "pong!"}
