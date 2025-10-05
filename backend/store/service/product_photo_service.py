from store.models import User


class FindByIdProductPhotoService:
    def find_by_id(self, token: str, user: User, product_photo_id: int) -> dict:
        pass


class FindAllForProductService:
    def find_all_for_product(self, token: str, user: User, validated_data: dict) -> list[dict]:
        pass


class CreateProductPhotoService:
    def create(self, token: str, user: User, new_product_photo_data: dict) -> str:
        pass


class DeleteProductPhotoService:
    def delete(self, token : str, user: User, product_photo_id: int) -> str:
        pass
