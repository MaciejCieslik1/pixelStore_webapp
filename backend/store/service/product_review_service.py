from django.core.paginator import Paginator

from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User


class FindByIdProductReviewService:
    def find_by_id(self, token: str, user: User, product_id: int) -> dict:
        pass


class FindAllProductReviewsService:
    def find_all(self, token: str, user: User, validated_data: dict) -> list[dict]:
        pass


class FindAllFromUserProductReviewsService:
    def find_all(self, token: str, user: User, validated_data: dict) -> list[dict]:
        pass


class CreateProductReviewService:
    def create(self, token: str, user: User, new_product_data: dict) -> str:
        pass


class DeleteProductReviewService:
    def delete(self, token : str, user: User, product_id: int) -> str:
        pass
