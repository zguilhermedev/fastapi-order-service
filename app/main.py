from fastapi import FastAPI
from app.api.routers.health import router as health_router

def create_application() -> FastAPI:
    app = FastAPI(
        title="FastAPI Order Service",
        version="0.1.0",
        description="API de gerenciamento de pedidos com FastAPI"
    )

    app.include_router(health_router)

    return app

app = create_application()