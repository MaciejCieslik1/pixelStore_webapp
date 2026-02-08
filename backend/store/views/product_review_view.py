from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.service.product_review_service import FindByIdProductReviewService, FindAllProductReviewsService, \
    FindAllFromUserProductReviewsService, CreateProductReviewService, DeleteProductReviewService


class FindByIdProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_product_review_service: FindByIdProductReviewService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_product_review_service = find_by_id_product_review_service

    @property
    def find_by_id_product_review_service(self):
        return self._find_by_id_product_review_service

    def get(self, request: Request, product_id: int) -> Response:
        pass


class FindAllProductReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_product_reviews_service: FindAllProductReviewsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_product_reviews_service = find_all_product_reviews_service

    @property
    def find_all_products_service(self):
        return self._find_all_product_reviews_service

    def get(self, request: Request) -> Response:
        pass


class FindAllFromUserProductReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_from_user_product_reviews_service: FindAllFromUserProductReviewsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_from_user_product_reviews_service = find_all_from_user_product_reviews_service

    @property
    def find_all_products_service(self):
        return self._find_all_from_user_product_reviews_service

    def get(self, request: Request) -> Response:
        pass


class CreateProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_product_review_service: CreateProductReviewService, **kwargs):
        super().__init__(**kwargs)
        self._create_product_review_service = create_product_review_service

    @property
    def create_product_service(self):
        return self._create_product_review_service

    def post(self, request: Request) -> Response:
        pass


class DeleteProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_product_review_service: DeleteProductReviewService, **kwargs):
        super().__init__(**kwargs)
        self._delete_product_review_service = delete_product_review_service

    @property
    def delete_product_service(self):
        return self._delete_product_review_service

    def delete(self, request: Request, product_review_id: int) -> Response:
        pass
