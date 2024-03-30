import logging

from fastapi import FastAPI

from challenge.routes import health, index, inference

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(index.router, tags=["index"])
    application.include_router(health.router, tags=["health"])
    application.include_router(inference.router, tags=["inference"])

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
