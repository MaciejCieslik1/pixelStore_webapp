from django.core.paginator import Paginator

from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User


class FindByIdTransactionService:
    def find_by_id(self, token: str, user: User, transaction_id: int) -> dict:
        pass


class FindAllMineTransactionsService:
    def find_all_mine(self, token: str, user: User, validated_data: dict) -> list[dict]:
        pass


class CreateTransactionService:
    def create(self, token: str, user: User, new_transaction_data: dict) -> str:
        pass

class UpdateTransactionService:
    def update(self, token : str, user: User, transaction_id: int) -> str:
        pass


class DeleteTransactionService:
    def delete(self, token : str, user: User, transaction_id: int) -> str:
        pass
