from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import CurrentUser, get_customer_service
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import (
    CustomerAlreadyExistsError,
    CustomerService,
)

router = APIRouter(prefix="/customers", tags=["customers"])

CustomerServiceDep = Annotated[CustomerService, Depends(get_customer_service)]


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    payload: CustomerCreate,
    service: CustomerServiceDep,
    current_user: CurrentUser,
) -> CustomerResponse:
    try:
        customer = service.create_customer(payload)
    except CustomerAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    return CustomerResponse.model_validate(customer)


@router.get(
    "",
    response_model=list[CustomerResponse],
    status_code=status.HTTP_200_OK,
)
def list_customers(service: CustomerServiceDep) -> list[CustomerResponse]:
    customers = service.list_customers()
    return [CustomerResponse.model_validate(customer) for customer in customers]


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
)
def get_customer_by_id(
    customer_id: int,
    service: CustomerServiceDep,
) -> CustomerResponse:
    customer = service.get_customer_by_id(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return CustomerResponse.model_validate(customer)