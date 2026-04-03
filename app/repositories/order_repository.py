from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models.order import Order


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, order: Order) -> Order:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def get_by_id(self, order_id: int) -> Order | None:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return self.session.scalar(stmt)

    def list_all(self) -> list[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .order_by(Order.id)
        )
        return list(self.session.scalars(stmt).all())