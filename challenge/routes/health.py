from fastapi import APIRouter, Depends

from challenge.config import Settings, get_settings

router = APIRouter()


@router.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@router.get("/ping", status_code=200)
async def pong(settings: Settings = Depends(get_settings)) -> dict:
    return {"ping": "pong!", "environment": settings.environment, "testing": settings.testing}
