from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/", status_code=200)
async def root() -> Dict[str, str]:
    """Root endpoint for the API.

    Returns
    -------
    Dict[str, str]
        Welcome message.
    """
    return {"message": "Welcome to SkyProphet!"}
