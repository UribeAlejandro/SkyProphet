from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200)
async def get_health() -> Dict[str, str]:
    """Health check endpoint.

    Returns
    -------
    dict
        Status of the API.
    """
    return {"status": "OK"}


@router.get("/ping", status_code=200)
async def pong() -> Dict[str, str]:
    """Ping endpoint.

    Returns
    -------
    dict
        Pong message.
    """
    return {"ping": "pong!"}
