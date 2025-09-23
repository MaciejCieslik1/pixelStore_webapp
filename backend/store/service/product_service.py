from store.models import User


class FindByIdProductService:
    def find_by_id(self, token: str, user: User, product_id: int) -> dict:
        pass


class FindAllProductsService:
    def find_all(self, token: str, user: User, validated_data: dict) -> list[dict]:
        pass


class CreateProductService:
    def create(self, token: str, user: User, new_product_data: dict) -> str:
        pass


class UpdateProductService:
    def update(self, token : str, user: User, product_id: int) -> str:
        pass


class DeleteProductService:
    def delete(self, token : str, user: User, product_id: int) -> str:
        pass
