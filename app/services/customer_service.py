from app.db.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate

class CustomerAlreadyExistsError(Exception):
    pass

class CustomerService:
    def __init__(self, repository: CustomerRepository) -> None:
        self.repository = repository

    def create_customer(self, payload: CustomerCreate) -> Customer:
        existing_customer = self.repository.get_by_email(payload.email)
        if existing_customer is not None:
            raise CustomerAlreadyExistsError(
                "Customer with this email already exists"
            )

        customer = Customer(
            name=payload.name,
            email=payload.email,
        )

        return self.repository.create(customer)

    def list_customers(self) -> list[Customer]:
        return self.repository.list_all()

    def get_customer_by_id(self, customer_id: int) -> Customer | None:
        return self.repository.get_by_id(customer_id)