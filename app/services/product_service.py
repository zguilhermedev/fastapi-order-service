from app.db.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate

class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def create_product(self, payload: ProductCreate) -> Product:
        product = Product(
            name=payload.name,
            description=payload.description,
            price=payload.price,
        )

        return self.repository.create(product)

    def list_products(self) -> list[Product]:
        return self.repository.list_all()

    def get_product_by_id(self, product_id: int) -> Product:
        return self.repository.get_by_id(product_id)