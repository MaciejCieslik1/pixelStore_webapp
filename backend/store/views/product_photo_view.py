from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.service.product_photo_service import FindByIdProductPhotoService, FindAllForProductService, \
    CreateProductPhotoService, DeleteProductPhotoService


class FindByIdProductPhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_product_photo_service: FindByIdProductPhotoService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_product_photo_service = find_by_id_product_photo_service

    @property
    def find_by_id_product_photo_service(self):
        return self._find_by_id_product_photo_service

    def get(self, request: Request, product_photo_id: int) -> Response:
        pass


class FindAllForProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_for_product_service: FindAllForProductService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_for_product_service = find_all_for_product_service

    @property
    def find_all_for_product_service(self):
        return self._find_all_for_product_service

    def get(self, request: Request) -> Response:
        pass


class CreateProductPhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_product_photo_service: CreateProductPhotoService, **kwargs):
        super().__init__(**kwargs)
        self._create_product_photo_service = create_product_photo_service

    @property
    def create_product_photo_service(self):
        return self._create_product_photo_service

    def post(self, request: Request) -> Response:
        pass


class DeleteProductPhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_product_photo_service: DeleteProductPhotoService, **kwargs):
        super().__init__(**kwargs)
        self._delete_product_photo_service = delete_product_photo_service

    @property
    def delete_product_photo_service(self):
        return self._delete_product_photo_service

    def delete(self, request: Request, product_photo_id: int) -> Response:
        pass
