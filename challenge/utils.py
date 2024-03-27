from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: str
    message: str
    data: dict = {}


class HealthResponse(BaseResponse):
    status: str = "OK"


class PredictResponse(BaseResponse):
    pass


class ErrorResponse(BaseResponse):
    pass


class PredictRequest(BaseModel):
    data: dict


class HealthRequest(BaseModel):
    pass
