from decimal import Decimal

from app.db.models.customer import Customer
from app.db.models.order import Order, OrderStatus
from app.db.models.order_item import OrderItem
from app.db.models.product import Product
from app.repositories.customer_repository import CustomerRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreate


class CustomerNotFoundError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        customer_repository: CustomerRepository,
        product_repository: ProductRepository,
    ) -> None:
        self.order_repository = order_repository
        self.customer_repository = customer_repository
        self.product_repository = product_repository

    def create_order(self, payload: OrderCreate) -> Order:
        customer = self.customer_repository.get_by_id(payload.customer_id)

        if customer is None:
            raise CustomerNotFoundError("Customer not found")

        order_items: list[OrderItem] = []
        total_amount = Decimal("0.00")

        for item_payload in payload.items:
            product = self.product_repository.get_by_id(item_payload.product_id)

            if product is None:
                raise ProductNotFoundError(
                    f"Product {item_payload.product_id} not found"
                )

            unit_price = product.price
            subtotal = unit_price * item_payload.quantity
            total_amount += subtotal

            order_item = OrderItem(
                product_id=product.id,
                quantity=item_payload.quantity,
                unit_price=unit_price,
                subtotal=subtotal,
            )
            order_items.append(order_item)

        order = Order(
            customer_id=customer.id,
            status=OrderStatus.CREATED,
            total_amount=total_amount,
            items=order_items,
        )

        return self.order_repository.create(order)

    def get_order_by_id(self, order_id: int) -> Order | None:
        return self.order_repository.get_by_id(order_id)

    def list_orders(self) -> list[Order]:
        return self.order_repository.list_all()