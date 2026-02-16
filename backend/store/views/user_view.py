from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.check_id_serializer import CheckIdSerializer
from store.serializers.page_serializer import PageSerializer
from store.serializers.transaction_serializer import CreateTransactionSerializer, UpdateTransactionSerializer
from store.service.transaction_service import FindByIdTransactionService, FindAllMineTransactionsService, \
    CreateTransactionService, UpdateTransactionService
from store.service.user_service import FindByUsernameUserService, UpdateUserService, DeleteAccountUserService


class FindByUsernameUserView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_username_user_service: FindByUsernameUserService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_username_user_service = find_by_username_user_service

    @property
    def find_by_username_user_service(self):
        return self._find_by_username_user_service

    def get(self, request: Request, username: str) -> Response:
        pass


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_user_service: UpdateUserService, **kwargs):
        super().__init__(**kwargs)
        self._update_user_service = update_user_service

    @property
    def update_user_service(self):
        return self._update_user_service

    def put(self, request: Request) -> Response:
        pass


class DeleteAccountUserView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_account_user_service: DeleteAccountUserService, **kwargs):
        super().__init__(**kwargs)
        self._delete_service = delete_account_user_service

    @property
    def delete_account_user_service(self):
        return self._delete_service

    def delete(self, request: Request) -> Response:
        pass
