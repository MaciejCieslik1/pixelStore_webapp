from store.models import User


class FindByIdOrderReturnService:
    def find_by_id(self, token: str, user: User, order_return_id: int) -> dict:
        pass


class CreateOrderReturnService:
    def create(self, token: str, user: User, new_order_return_data: dict) -> str:
        pass


class UpdateOrderReturnService:
    def update(self, token : str, user: User, order_return_id: int) -> str:
        pass
