from store.models import User


class FindByIdOrderProductService:
    def find_by_id(self, token: str, user: User, order_product_id: int) -> dict:
        pass

class CreateOrderProductService:
    def create(self, token: str, user: User, new_order_product_data: dict) -> str:
        pass


class UpdateOrderProductService:
    def update(self, token: str,user: User, updated_order_product_data: dict) -> str:
        pass


class DeleteOrderProductService:
    def delete(self, token : str, user: User, order_product_id: int) -> str:
        pass
