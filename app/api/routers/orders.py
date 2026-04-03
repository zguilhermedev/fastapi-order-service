from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import CurrentUser, get_order_service
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import (
    CustomerNotFoundError,
    OrderService,
    ProductNotFoundError,
)

router = APIRouter(prefix="/orders", tags=["orders"])

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    payload: OrderCreate,
    service: OrderServiceDep,
    current_user: CurrentUser,
) -> OrderResponse:
    try:
        order = service.create_order(payload)
    except CustomerNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return OrderResponse.model_validate(order)


@router.get(
    "",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
def list_orders(
    service: OrderServiceDep,
    current_user: CurrentUser,
) -> list[OrderResponse]:
    orders = service.list_orders()
    return [OrderResponse.model_validate(order) for order in orders]


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def get_order_by_id(
    order_id: int,
    service: OrderServiceDep,
    current_user: CurrentUser,
) -> OrderResponse:
    order = service.get_order_by_id(order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return OrderResponse.model_validate(order)