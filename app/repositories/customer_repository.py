from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.customer import Customer

class CustomerRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, customer: Customer) -> Customer:
        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def list_all(self) -> list[Customer]:
        stmt = select(Customer).order_by(Customer.id)
        return list(self.session.scalars(stmt))

    def get_by_id(self, customer_id: int) -> Customer | None:
        stmt = select(Customer).where(Customer.id == customer_id)
        return self.session.scalar(stmt)
    
    def get_by_email(self, email: str) -> Customer | None:
        stmt = select(Customer).where(Customer.email == email)
        return self.session.scalar(stmt)