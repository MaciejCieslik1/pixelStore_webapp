import datetime

from django.core.paginator import Paginator
from django.db.models import Q

from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, Transaction, OrderProduct
from store.output_serializers.transaction_output_serializer import TransactionOutputSerializer


class FindByUsernameUserService:
    def find_by_username(self, token: str, user: User, username: str) -> dict:
        pass


class UpdateUserService:
    def update(self, token : str, user: User, update_data: dict) -> str:
        pass


class DeleteAccountUserService:
    def delete(self, token : str, user: User) -> str:
        pass
