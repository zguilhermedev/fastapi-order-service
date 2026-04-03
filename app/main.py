from fastapi import FastAPI
from app.api.routers.health import router as health_router
from app.api.routers.products import router as products_router
from app.api.routers.auth import router as auth_router
from app.api.routers.customers import router as customers_router
from app.core.config import settings

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="API de gerenciamento de pedidos com FastAPI"
    )

    app.include_router(health_router)
    app.include_router(products_router)
    app.include_router(auth_router)
    app.include_router(customers_router)

    return app

app = create_application()