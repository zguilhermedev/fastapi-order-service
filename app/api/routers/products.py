from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import CurrentUser, get_product_service
from app.db.models.user import User
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: ProductCreate,
    service: ProductServiceDep,
    current_user: CurrentUser,
) -> ProductResponse:
    product = service.create_product(payload)
    return ProductResponse.model_validate(product)


@router.get(
    "",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
)
def list_products(service: ProductServiceDep) -> list[ProductResponse]:
    products = service.list_products()
    return [ProductResponse.model_validate(product) for product in products]


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
def get_product_by_id(
    product_id: int,
    service: ProductServiceDep,
) -> ProductResponse:
    product = service.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return ProductResponse.model_validate(product)