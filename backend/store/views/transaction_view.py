from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.service.transaction_service import FindByIdTransactionService, FindAllMineTransactionsService, \
    CreateTransactionService, UpdateTransactionService, DeleteTransactionService


class FindByIdTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_transaction_service: FindByIdTransactionService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_transaction_service = find_by_id_transaction_service

    @property
    def find_by_id_transaction_service(self):
        return self._find_by_id_transaction_service

    def get(self, request: Request, transaction_id: int) -> Response:
        pass


class FindAllMineTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_mine_transactions_service: FindAllMineTransactionsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_mine_transactions_service = find_all_mine_transactions_service

    @property
    def find_all_mine_transactions_service(self):
        return self._find_all_mine_transactions_service

    def get(self, request: Request) -> Response:
        pass


class CreateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_transaction_service: CreateTransactionService, **kwargs):
        super().__init__(**kwargs)
        self._create_transaction_service = create_transaction_service

    @property
    def create_transaction_service(self):
        return self._create_transaction_service

    def post(self, request: Request) -> Response:
        pass


class UpdateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_transaction_service: UpdateTransactionService, **kwargs):
        super().__init__(**kwargs)
        self._update_transaction_service = update_transaction_service

    @property
    def update_transaction_service(self):
        return self._update_transaction_service

    def put(self, request: Request, product_id: int) -> Response:
        pass


class DeleteTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_transaction_service: DeleteTransactionService, **kwargs):
        super().__init__(**kwargs)
        self._delete_transaction_service = delete_transaction_service

    @property
    def delete_transaction_service(self):
        return self._delete_transaction_service

    def delete(self, request: Request, product_id: int) -> Response:
        pass
