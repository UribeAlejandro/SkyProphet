from fastapi import APIRouter
from fastapi.responses import JSONResponse

from challenge.models.features import DelayResponse, PayloadFeatures

router = APIRouter()


@router.post("/predict", status_code=200, response_model=DelayResponse)
async def post_predict(payload: PayloadFeatures) -> JSONResponse:
    # TODO: process the payload and modify the response
    payload = payload.dict()
    preds = DelayResponse(predict=[0])
    return JSONResponse(content=preds.model_dump())
