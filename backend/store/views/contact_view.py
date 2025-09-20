from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, CategoryNotFoundError, CategoryNameAlreadyOccupiedError
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.category_serializer import FindCategoryByNameSerializer, CreateCategorySerializer
from store.service.category_service import FindCategoryByNameService, FindAllCategoriesService, CreateCategoryService
from store.service.contact_service import FindContactByNameService, FindAllContactsService, CreateContactService, \
    DeleteContactByNameService


class FindContactByNameView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_contact_by_name_service: FindContactByNameService, **kwargs):
        super().__init__(**kwargs)
        self._find_contact_by_name_service = find_contact_by_name_service

    @property
    def find_contact_by_name_service(self):
        return self._find_contact_by_name_service

    def get(self, request: Request, username: str) -> Response:
        pass


class FindAllContactsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_contacts_service: FindAllContactsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_contacts_service = find_all_contacts_service

    @property
    def find_all_contacts_service(self):
        return self._find_all_contacts_service

    def get(self, request: Request) -> Response:
        pass


class CreateContactView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_contact_service: CreateContactService, **kwargs):
        super().__init__(**kwargs)
        self._create_contact_service = create_contact_service

    @property
    def create_contact_service(self):
        return self._create_contact_service

    def post(self, request: Request) -> Response:
        pass


class DeleteContactByNameView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_contact_service: DeleteContactByNameService, **kwargs):
        super().__init__(**kwargs)
        self._delete_contact_service = delete_contact_service

    @property
    def delete_contact_service(self):
        return self._delete_contact_service

    def delete(self, request: Request, username: str) -> Response:
        pass
