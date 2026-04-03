from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.product import Product

class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def list_all(self) -> list[Product]:
        stmt = select(Product).order_by(Product.id)
        return list(self.session.scalars(stmt).all())

    def get_by_id(self, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        return self.session.scalar(stmt)