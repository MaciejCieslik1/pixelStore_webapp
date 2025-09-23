from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.service.product_service import FindByIdProductService, FindAllProductsService, CreateProductService, \
    UpdateProductService, DeleteProductService


class FindByIdProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_product_service: FindByIdProductService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_product_service = find_by_id_product_service

    @property
    def find_by_id_product_service(self):
        return self._find_by_id_product_service

    def get(self, request: Request, product_id: int) -> Response:
        pass


class FindAllProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_products_service: FindAllProductsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_products_service = find_all_products_service

    @property
    def find_all_products_service(self):
        return self._find_all_products_service

    def get(self, request: Request) -> Response:
        pass


class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_product_service: CreateProductService, **kwargs):
        super().__init__(**kwargs)
        self._create_product_service = create_product_service

    @property
    def create_product_service(self):
        return self._create_product_service

    def post(self, request: Request) -> Response:
        pass


class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_product_service: UpdateProductService, **kwargs):
        super().__init__(**kwargs)
        self._update_product_service = update_product_service

    @property
    def update_product_service(self):
        return self._update_product_service

    def put(self, request: Request, product_id: int) -> Response:
        pass


class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_product_service: DeleteProductService, **kwargs):
        super().__init__(**kwargs)
        self._delete_product_service = delete_product_service

    @property
    def delete_product_service(self):
        return self._delete_product_service

    def delete(self, request: Request, product_id: int) -> Response:
        pass
