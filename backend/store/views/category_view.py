from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.service.category_service import FindCategoryByNameService, FindAllCategoriesService, CreateCategoryService


class FindCategoryByNameView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_category_by_name_service: FindCategoryByNameService, **kwargs):
        super().__init__(**kwargs)
        self._find_category_by_name_service = find_category_by_name_service

    @property
    def find_category_by_name_service(self):
        return self._find_category_by_name_service

    def get(self, request: Request, name: str) -> Response:
        pass


class FindAllCategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_categories_service: FindAllCategoriesService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_categories_service = find_all_categories_service

    @property
    def find_all_categories_service(self):
        return self._find_all_categories_service

    def get(self, request: Request) -> Response:
        pass


class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_category_service: CreateCategoryService, **kwargs):
        super().__init__(**kwargs)
        self._create_category_service = create_category_service

    @property
    def create_category_service(self):
        return self._create_category_service

    def post(self, request: Request) -> Response:
        pass
