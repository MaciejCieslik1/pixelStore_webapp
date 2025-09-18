from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.service.order_return_service import FindByIdOrderReturnService, UpdateOrderReturnService, \
    CreateOrderReturnService


class FindByIdOrderReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_order_return_service: FindByIdOrderReturnService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_order_return_service = find_by_id_order_return_service

    @property
    def find_by_id_order_return_service(self):
        return self._find_by_id_order_return_service

    def get(self, request: Request, order_return_id: int) -> Response:
        pass


class CreateOrderReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_order_return_service: CreateOrderReturnService, **kwargs):
        super().__init__(**kwargs)
        self._create_order_return_service = create_order_return_service

    @property
    def create_order_return_service(self):
        return self._create_order_return_service

    def post(self, request: Request) -> Response:
        pass


class UpdateOrderReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_order_return_service: UpdateOrderReturnService, **kwargs):
        super().__init__(**kwargs)
        self._update_order_return_service = update_order_return_service

    @property
    def update_order_return_service(self):
        return self._update_order_return_service

    def update(self, request: Request, order_return_id: int) -> Response:
        pass