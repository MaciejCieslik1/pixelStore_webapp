from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.service.order_product_service import FindByIdOrderProductService, CreateOrderProductService, \
    UpdateOrderProductService, DeleteOrderProductService


class FindByIdOrderProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_order_product_service: FindByIdOrderProductService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_order_product_service = find_by_id_order_product_service

    @property
    def find_by_id_order_product_service(self):
        return self._find_by_id_order_product_service

    def get(self, request: Request, order_product_id: int) -> Response:
        pass


class CreateOrderProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_order_product_service: CreateOrderProductService, **kwargs):
        super().__init__(**kwargs)
        self._create_order_product_service = create_order_product_service

    @property
    def create_order_product_service(self):
        return self._create_order_product_service

    def post(self, request: Request) -> Response:
        pass


class UpdateOrderProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_order_product_service: UpdateOrderProductService, **kwargs):
        super().__init__(**kwargs)
        self._update_order_product_service = update_order_product_service

    @property
    def update_order_product_service(self):
        return self._update_order_product_service

    def update(self, request: Request) -> Response:
        pass


class DeleteOrderProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_order_product_service: DeleteOrderProductService, **kwargs):
        super().__init__(**kwargs)
        self._delete_order_product_service = delete_order_product_service

    @property
    def delete_order_product_service(self):
        return self._delete_order_product_service

    def delete(self, request: Request) -> Response:
        pass
