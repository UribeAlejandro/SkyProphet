from fastapi import APIRouter
from fastapi.responses import JSONResponse

from challenge.models.features import DelayResponse, PayloadFeatures
from challenge.pipeline.serving import inference_pipeline

router = APIRouter()


@router.post("/predict", status_code=200, response_model=DelayResponse)
async def post_predict(payload: PayloadFeatures) -> JSONResponse:
    """Predict delay for flights.

    Parameters
    ----------
    payload : PayloadFeatures
        Payload with flights data.

    Returns
    -------
    JSONResponse
        Predicted delays.
    """
    payload = payload.dict()
    delay_preds = inference_pipeline(payload)
    delay_reponse = DelayResponse(predict=delay_preds)

    return JSONResponse(content=delay_reponse.model_dump())
